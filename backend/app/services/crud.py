from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from .. import models, schemas
from .deduplication import compute_fingerprint, is_duplicate


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    from ..auth.security import get_password_hash

    user = models.User(email=user_in.email, hashed_password=get_password_hash(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_calls(
    db: Session,
    filters: schemas.CallFilter,
    page: int = 1,
    size: int = 20,
) -> Tuple[List[models.Call], int]:
    query = select(models.Call)
    if filters.country:
        query = query.filter(models.Call.country.ilike(f"%{filters.country}%"))
    if filters.funding_type:
        query = query.filter(models.Call.funding_type == filters.funding_type)
    if filters.amount_min:
        query = query.filter(models.Call.amount >= filters.amount_min)
    if filters.amount_max:
        query = query.filter(models.Call.amount <= filters.amount_max)
    if filters.closing_before:
        query = query.filter(models.Call.deadline <= filters.closing_before)
    if filters.closing_after:
        query = query.filter(models.Call.deadline >= filters.closing_after)
    query = query.order_by(models.Call.deadline.asc().nulls_last())

    total = db.scalar(select(func.count()).select_from(query.subquery()))
    calls = db.execute(query.offset((page - 1) * size).limit(size)).scalars().all()
    return calls, total


def get_call(db: Session, call_id: int) -> Optional[models.Call]:
    return db.get(models.Call, call_id)


def create_or_update_call(db: Session, source: models.Source, payload: dict) -> Tuple[models.Call, bool]:
    fingerprint = compute_fingerprint(
        title=payload["title"],
        deadline=payload.get("deadline"),
        organizer=payload["organizer"],
        amount=payload.get("amount"),
    )
    existing = db.query(models.Call).filter(models.Call.fingerprint_hash == fingerprint).one_or_none()
    created = False
    if existing:
        updated_fields = {}
        for key, value in payload.items():
            if getattr(existing, key) != value and value is not None:
                updated_fields[key] = value
                setattr(existing, key, value)
        if updated_fields:
            version = models.CallVersion(call=existing, data=updated_fields)
            existing.last_scraped_at = datetime.utcnow()
            db.add(version)
    else:
        existing = models.Call(**payload, source=source, fingerprint_hash=fingerprint)
        db.add(existing)
        created = True
    db.commit()
    db.refresh(existing)
    return existing, created


def create_alert(db: Session, user: models.User, alert_in: schemas.AlertCreate) -> models.Alert:
    alert = models.Alert(user=user, filters=alert_in.filters.dict(exclude_none=True), channel=alert_in.channel)
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def list_sources(db: Session) -> List[models.Source]:
    return db.execute(select(models.Source)).scalars().all()


def create_source(db: Session, source_in: schemas.SourceBase) -> models.Source:
    source = models.Source(**source_in.dict())
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


def record_scrape_log(
    db: Session,
    source: models.Source,
    status: str,
    started_at: datetime,
    finished_at: datetime,
    stats: dict,
    error: Optional[str] = None,
) -> models.ScrapeLog:
    log = models.ScrapeLog(
        source=source,
        started_at=started_at,
        finished_at=finished_at,
        status=status,
        items_fetched=stats.get("fetched", 0),
        items_created=stats.get("created", 0),
        items_updated=stats.get("updated", 0),
        error_message=error,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_latest_scrape_logs(db: Session) -> List[dict]:
    subquery = (
        select(
            models.ScrapeLog.source_id.label("source_id"),
            func.max(models.ScrapeLog.started_at).label("last_started_at"),
        )
        .group_by(models.ScrapeLog.source_id)
        .subquery()
    )

    stmt = (
        select(models.Source, models.ScrapeLog)
        .join(subquery, models.Source.id == subquery.c.source_id, isouter=True)
        .join(
            models.ScrapeLog,
            (models.ScrapeLog.source_id == subquery.c.source_id)
            & (models.ScrapeLog.started_at == subquery.c.last_started_at),
            isouter=True,
        )
        .order_by(models.Source.name)
    )

    return [
        {"source": source, "log": log}
        for source, log in db.execute(stmt).all()
    ]


def add_favorite(db: Session, user: models.User, call: models.Call) -> models.Favorite:
    favorite = models.Favorite(user=user, call=call)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite


def get_metrics(db: Session) -> dict:
    successes = db.scalar(select(func.count()).select_from(models.ScrapeLog).filter(models.ScrapeLog.status == "success")) or 0
    failures = db.scalar(select(func.count()).select_from(models.ScrapeLog).filter(models.ScrapeLog.status == "failed")) or 0
    last_scrape = db.scalar(select(func.max(models.ScrapeLog.finished_at)))
    return {"scrapes_success": successes, "scrapes_failed": failures, "last_scrape": last_scrape}
