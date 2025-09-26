from __future__ import annotations
from typing import List
import requests
from datetime import datetime

from ..base import BaseScraper


class APIScraper(BaseScraper):
    """Scraper que consume APIs o feeds RSS."""

    def fetch(self) -> List[dict]:
        response = requests.get(self.url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("calls", [])

    def normalize(self, item: dict) -> dict:
        def parse_iso(value: str | None):
            if not value:
                return None
            value = value.replace("Z", "+00:00")
            return datetime.fromisoformat(value)

        deadline = parse_iso(item.get("deadline"))
        published = parse_iso(item.get("published_at")) or datetime.utcnow()
        return {
            "origin_id": item["id"],
            "title": item["title"],
            "description": item.get("description", ""),
            "organizer": item.get("organizer", ""),
            "country": item.get("country", ""),
            "region": item.get("region"),
            "published_at": published.date(),
            "deadline": deadline.date() if deadline else None,
            "amount": item.get("amount"),
            "currency": item.get("currency"),
            "funding_type": item.get("funding_type", "subvencion"),
            "requirements": item.get("requirements", []),
            "source_url": item.get("url"),
            "tags": item.get("tags", []),
        }
