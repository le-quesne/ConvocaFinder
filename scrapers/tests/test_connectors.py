from unittest.mock import patch
import json

from scrapers.connectors.static_html import StaticHTMLScraper
from scrapers.connectors.api_client import APIScraper
from scrapers.connectors.dynamic_playwright import DynamicPlaywrightScraper

HTML_SNIPPET = """
<div class="call-card">
    <h3>Convocatoria Test</h3>
    <a href="https://example.com/call/1">Ver más</a>
    <span class="organizer">Ministerio X</span>
    <span class="deadline">2025-12-31</span>
    <span class="country">Chile</span>
    <p class="description">Descripción breve</p>
</div>
"""


def test_static_html_scraper_parses_items():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = HTML_SNIPPET
        scraper = StaticHTMLScraper("https://example.com")
        items = scraper.fetch()
        assert len(items) == 1
        normalized = scraper.normalize(items[0])
        assert normalized["title"] == "Convocatoria Test"
        assert normalized["funding_type"] == "subvencion"


def test_api_scraper_normalizes():
    payload = {
        "calls": [
            {
                "id": "orig-12345",
                "title": "Convocatoria Nacional de Innovación 2025",
                "description": "Beca para proyectos...",
                "organizer": "Ministerio de Ciencia",
                "country": "Chile",
                "region": "Región Metropolitana",
                "published_at": "2025-09-01T00:00:00",
                "deadline": "2025-10-15T00:00:00",
                "amount": 500000,
                "currency": "CLP",
                "funding_type": "subvencion",
                "requirements": ["ser pyme", "tener RUT"],
                "url": "https://fondos.gob.cl/convocatoria/123",
                "tags": ["innovacion", "tecnologia"],
            }
        ]
    }
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = payload
        scraper = APIScraper("https://api.example.com")
        items = scraper.fetch()
        normalized = scraper.normalize(items[0])
        assert normalized["origin_id"] == "orig-12345"
        assert normalized["country"] == "Chile"


def test_dynamic_scraper_normalize_only():
    scraper = DynamicPlaywrightScraper("https://spa.example.com")
    item = {
        "title": "F6S Challenge",
        "url": "https://spa.example.com/call",
        "organizer": "F6S",
        "deadline": "01/12/2025",
        "country": "Global",
        "description": "Programa de aceleración",
    }
    normalized = scraper.normalize(item)
    assert normalized["funding_type"] == "aceleradora"
    assert normalized["deadline"].year == 2025
