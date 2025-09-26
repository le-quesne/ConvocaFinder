from datetime import date
from typing import Optional
from rapidfuzz import fuzz
import hashlib


def compute_fingerprint(title: str, deadline: Optional[date], organizer: str, amount: Optional[float]) -> str:
    parts = [title.strip().lower(), organizer.strip().lower()]
    parts.append(deadline.isoformat() if deadline else "none")
    parts.append(str(int(amount)) if amount else "0")
    joined = "|".join(parts)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


def is_duplicate(existing_title: str, new_title: str, threshold: int = 90) -> bool:
    similarity = fuzz.token_sort_ratio(existing_title, new_title)
    return similarity >= threshold
