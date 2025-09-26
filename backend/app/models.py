from __future__ import annotations
from datetime import datetime, date
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    Boolean,
    ForeignKey,
    Numeric,
    UniqueConstraint,
    JSON,
)
from sqlalchemy.orm import relationship

from .core.database import Base


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")


class Source(Base, TimestampMixin):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False)
    type = Column(String(100), nullable=False)
    access_method = Column(String(100), nullable=False)
    frequency_hours = Column(Integer, nullable=False, default=24)
    is_active = Column(Boolean, default=True, nullable=False)
    robots_status = Column(String(50), default="unknown", nullable=False)
    tos_notes = Column(Text, default="", nullable=False)

    convocatorias = relationship("Call", back_populates="source")
    logs = relationship("ScrapeLog", back_populates="source")


class Call(Base, TimestampMixin):
    __tablename__ = "calls"
    __table_args__ = (
        UniqueConstraint("fingerprint_hash", name="uq_calls_fingerprint"),
    )

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    origin_id = Column(String(255), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    organizer = Column(String(255), nullable=False)
    country = Column(String(100), nullable=False)
    region = Column(String(100))
    published_at = Column(Date, nullable=False)
    deadline = Column(Date)
    amount = Column(Numeric(precision=14, scale=2))
    currency = Column(String(10))
    funding_type = Column(String(100), nullable=False)
    requirements = Column(JSON, nullable=False, default=list)
    source_url = Column(String(500), nullable=False)
    tags = Column(JSON, nullable=False, default=list)
    last_scraped_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    fingerprint_hash = Column(String(255), nullable=False)

    source = relationship("Source", back_populates="convocatorias")
    versions = relationship("CallVersion", back_populates="call", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="call", cascade="all, delete-orphan")


class CallVersion(Base):
    __tablename__ = "call_versions"

    id = Column(Integer, primary_key=True)
    call_id = Column(Integer, ForeignKey("calls.id"), nullable=False)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    call = relationship("Call", back_populates="versions")


class ScrapeLog(Base, TimestampMixin):
    __tablename__ = "scrape_logs"

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=False)
    finished_at = Column(DateTime(timezone=True))
    status = Column(String(50), nullable=False)
    items_fetched = Column(Integer, default=0)
    items_created = Column(Integer, default=0)
    items_updated = Column(Integer, default=0)
    error_message = Column(Text)

    source = relationship("Source", back_populates="logs")


class Alert(Base, TimestampMixin):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filters = Column(JSON, nullable=False)
    channel = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    user = relationship("User", back_populates="alerts")


class Favorite(Base, TimestampMixin):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    call_id = Column(Integer, ForeignKey("calls.id"), nullable=False)

    user = relationship("User", back_populates="favorites")
    call = relationship("Call", back_populates="favorites")
