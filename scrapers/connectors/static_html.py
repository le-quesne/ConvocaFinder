from __future__ import annotations
from typing import List
from bs4 import BeautifulSoup
import requests
from datetime import datetime

from ..base import BaseScraper


class StaticHTMLScraper(BaseScraper):
    """Scraper para sitios con HTML estático (ej. portal estatal)."""

    def fetch(self) -> List[dict]:
        response = requests.get(self.url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.select("div.call-card")
        items = []
        for card in cards:
            items.append(
                {
                    "title": card.select_one("h3").get_text(strip=True),
                    "url": card.select_one("a")['href'],
                    "organizer": card.select_one("span.organizer").get_text(strip=True),
                    "deadline": card.select_one("span.deadline").get_text(strip=True),
                    "country": card.select_one("span.country").get_text(strip=True),
                    "description": card.select_one("p.description").get_text(strip=True),
                }
            )
        return items

    def normalize(self, item: dict) -> dict:
        deadline = datetime.strptime(item["deadline"], "%Y-%m-%d").date() if item.get("deadline") else None
        return {
            "origin_id": item["url"],
            "title": item["title"],
            "description": item.get("description", ""),
            "organizer": item["organizer"],
            "country": item.get("country", ""),
            "region": None,
            "published_at": deadline or datetime.utcnow().date(),
            "deadline": deadline,
            "amount": None,
            "currency": None,
            "funding_type": "subvencion",
            "requirements": [],
            "source_url": item["url"],
            "tags": [],
        }
