from datetime import date, datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from ..main import app
from ..core.database import Base, get_db
from ..services.deduplication import compute_fingerprint
from .. import models
from ..auth.security import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def seed_user(db):
    user = models.User(email="test@example.com", hashed_password=get_password_hash("password123"))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def seed_source(db):
    source = models.Source(
        name="Fuente Test",
        url="https://example.com",
        type="api",
        access_method="API",
        frequency_hours=24,
        is_active=True,
        robots_status="allowed",
        tos_notes="Uso permitido",
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


def test_create_and_list_call():
    db = TestingSessionLocal()
    user = seed_user(db)
    source = seed_source(db)
    payload = {
        "source_id": source.id,
        "origin_id": "orig-12345",
        "title": "Convocatoria Nacional de Innovación 2025",
        "description": "Beca para proyectos...",
        "organizer": "Ministerio de Ciencia",
        "country": "Chile",
        "region": "Región Metropolitana",
        "published_at": date(2025, 9, 1),
        "deadline": date(2025, 10, 15),
        "amount": 500000,
        "currency": "CLP",
        "funding_type": "subvencion",
        "requirements": ["ser pyme", "tener RUT"],
        "source_url": "https://fondos.gob.cl/convocatoria/123",
        "tags": ["innovacion", "tecnologia"],
        "last_scraped_at": datetime(2025, 9, 26, 10, 0, 0),
    }
    fingerprint = compute_fingerprint(payload["title"], payload["deadline"], payload["organizer"], payload["amount"])
    call = models.Call(**payload, fingerprint_hash=fingerprint)
    db.add(call)
    db.commit()
    db.refresh(call)

    response = client.get("/convocatorias")
    assert response.status_code == 200
    data = response.json()
    assert data["pagination"]["total"] == 1
    assert data["data"][0]["title"] == payload["title"]

    login = client.post("/auth/login", data={"username": user.email, "password": "password123"})
    token = login.json()["access_token"]
    favorite = client.post(
        f"/convocatorias/{call.id}/favorite",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert favorite.status_code == 200
