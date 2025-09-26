from datetime import date, datetime
from typing import List, Optional, Any
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserRead(UserBase, ORMModel):
    id: int
    is_active: bool
    is_admin: bool


class SourceBase(BaseModel):
    name: str
    url: str
    type: str
    access_method: str
    frequency_hours: int
    is_active: bool = True
    robots_status: str = "unknown"
    tos_notes: str = ""


class SourceRead(SourceBase, ORMModel):
    id: int


class Requirement(BaseModel):
    text: str


class CallBase(BaseModel):
    origin_id: str
    title: str
    description: str
    organizer: str
    country: str
    region: Optional[str]
    published_at: date
    deadline: Optional[date]
    amount: Optional[float]
    currency: Optional[str]
    funding_type: str
    requirements: List[str] = []
    source_url: str
    tags: List[str] = []


class CallRead(CallBase, ORMModel):
    id: int
    source_id: int
    last_scraped_at: datetime


class CallFilter(BaseModel):
    country: Optional[str] = None
    industry: Optional[str] = None
    amount_min: Optional[float] = None
    amount_max: Optional[float] = None
    stage: Optional[str] = None
    closing_before: Optional[date] = None
    closing_after: Optional[date] = None
    funding_type: Optional[str] = None


class AlertCreate(BaseModel):
    filters: CallFilter
    channel: str


class AlertRead(AlertCreate, ORMModel):
    id: int
    is_active: bool


class FavoriteCreate(BaseModel):
    call_id: int


class FavoriteRead(ORMModel):
    id: int
    call: CallRead


class Pagination(BaseModel):
    total: int
    page: int
    size: int


class PaginatedCalls(BaseModel):
    data: List[CallRead]
    pagination: Pagination


class ScrapeLogRead(ORMModel):
    id: int
    source_id: int
    started_at: datetime
    finished_at: Optional[datetime]
    status: str
    items_fetched: int
    items_created: int
    items_updated: int
    error_message: Optional[str]


class MetricsResponse(BaseModel):
    scrapes_success: int
    scrapes_failed: int
    last_scrape: Optional[datetime]
