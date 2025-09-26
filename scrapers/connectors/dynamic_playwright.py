from __future__ import annotations
from typing import List
from datetime import datetime
from playwright.sync_api import sync_playwright

from ..base import BaseScraper


class DynamicPlaywrightScraper(BaseScraper):
    """Scraper para aplicaciones SPA utilizando Playwright."""

    def fetch(self) -> List[dict]:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.url, wait_until="networkidle")
            items = page.evaluate(
                """
                () => {
                    return Array.from(document.querySelectorAll('[data-call]')).map(el => ({
                        title: el.querySelector('.title').innerText,
                        url: el.querySelector('a').href,
                        organizer: el.querySelector('.organizer').innerText,
                        deadline: el.querySelector('.deadline').dataset.date,
                        country: el.querySelector('.country').innerText,
                        description: el.querySelector('.description').innerText,
                    }));
                }
                """
            )
            browser.close()
        return items

    def normalize(self, item: dict) -> dict:
        deadline = datetime.strptime(item["deadline"], "%d/%m/%Y").date() if item.get("deadline") else None
        return {
            "origin_id": item["url"],
            "title": item["title"],
            "description": item.get("description", ""),
            "organizer": item["organizer"],
            "country": item.get("country", ""),
            "region": None,
            "published_at": datetime.utcnow().date(),
            "deadline": deadline,
            "amount": None,
            "currency": None,
            "funding_type": "aceleradora",
            "requirements": [],
            "source_url": item["url"],
            "tags": [],
        }
