from __future__ import annotations
from typing import Any, Iterable
from abc import ABC, abstractmethod


class BaseScraper(ABC):
    def __init__(self, url: str) -> None:
        self.url = url

    @abstractmethod
    def fetch(self) -> Iterable[Any]:
        raise NotImplementedError

    @abstractmethod
    def normalize(self, item: Any) -> dict:
        raise NotImplementedError

    def robots_allowed(self) -> bool:
        """Stub para validar robots.txt (simplificado)."""
        return True
