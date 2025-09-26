from __future__ import annotations
from datetime import datetime
from typing import Callable, Dict, List
import importlib
from sqlalchemy.orm import Session

from ..core.database import SessionLocal
from ..core.config import get_settings
from .. import models
from . import crud
from .notifications import NotificationService

try:  # pragma: no cover - import guard
    from ..main import scrape_success_counter, scrape_failed_counter
except Exception:  # pragma: no cover - fallback for tests
    scrape_success_counter = None
    scrape_failed_counter = None

settings = get_settings()
notification_service = NotificationService()


class ScraperRegistry:
    def __init__(self) -> None:
        self._registry: Dict[str, str] = {}

    def register(self, source_type: str, dotted_path: str) -> None:
        self._registry[source_type] = dotted_path

    def get(self, source_type: str):
        if source_type not in self._registry:
            raise KeyError(f"Scraper no registrado para tipo {source_type}")
        module_name, class_name = self._registry[source_type].rsplit(".", 1)
        module = importlib.import_module(module_name)
        return getattr(module, class_name)


registry = ScraperRegistry()
registry.register("html_static", "scrapers.connectors.static_html.StaticHTMLScraper")
registry.register("html_dynamic", "scrapers.connectors.dynamic_playwright.DynamicPlaywrightScraper")
registry.register("api", "scrapers.connectors.api_client.APIScraper")


def run_scraper_for_source(source_id: int) -> dict:
    db: Session = SessionLocal()
    source = db.get(models.Source, source_id)
    if not source or not source.is_active:
        return {"status": "skipped", "reason": "inactive"}
    started_at = datetime.utcnow()
    stats = {"fetched": 0, "created": 0, "updated": 0}
    error: str | None = None
    status = "success"
    try:
        scraper_cls = registry.get(source.type)
        scraper = scraper_cls(source.url)
        items = scraper.fetch()
        stats["fetched"] = len(items)
        for item in items:
            payload = scraper.normalize(item)
            payload.update({
                "source_id": source.id,
                "last_scraped_at": datetime.utcnow(),
            })
            call, created = crud.create_or_update_call(db, source, payload)
            stats["created" if created else "updated"] += 1
            if created:
                alerts = db.query(models.Alert).filter(models.Alert.is_active == True).all()  # noqa: E712
                recipients = [alert.user.email for alert in alerts if alert.channel == "email"]
                notification_service.notify_call({
                    "title": call.title,
                    "source_url": call.source_url,
                    "deadline": call.deadline.isoformat() if call.deadline else None,
                    "country": call.country,
                    "amount": float(call.amount) if call.amount else None,
                }, recipients)
    except Exception as exc:  # pragma: no cover - logging path
        status = "failed"
        error = str(exc)
        db.rollback()
        if scrape_failed_counter:
            scrape_failed_counter.inc()
    finally:
        finished_at = datetime.utcnow()
        crud.record_scrape_log(db, source, status, started_at, finished_at, stats, error)
        db.close()
        if status == "success" and scrape_success_counter:
            scrape_success_counter.inc()
    return {"status": status, "stats": stats, "error": error}


def run_all_scrapers() -> List[dict]:
    db: Session = SessionLocal()
    try:
        sources = db.query(models.Source).filter(models.Source.is_active == True).all()  # noqa: E712
        results = []
        for source in sources:
            results.append(run_scraper_for_source(source.id))
        return results
    finally:
        db.close()
