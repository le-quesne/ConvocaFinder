from datetime import date

from ..services.deduplication import compute_fingerprint, is_duplicate


def test_compute_fingerprint_changes_with_data():
    fp1 = compute_fingerprint("Titulo", date(2025, 1, 1), "Org", 1000)
    fp2 = compute_fingerprint("Titulo", date(2025, 1, 2), "Org", 1000)
    assert fp1 != fp2


def test_is_duplicate_threshold():
    title_a = "Convocatoria Innovación 2025"
    title_b = "Innovacion 2025 Convocatoria"
    assert is_duplicate(title_a, title_b)


def test_is_not_duplicate_when_low_similarity():
    title_a = "Convocatoria Salud"
    title_b = "Programa Turismo"
    assert not is_duplicate(title_a, title_b)
