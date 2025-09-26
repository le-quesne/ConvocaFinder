from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..services import crud
from .deps import get_admin_user_dep, get_db_dep

router = APIRouter(prefix="/scrape-logs", tags=["scrape-logs"])


@router.get("", response_model=list[schemas.SourceScrapeLog])
def get_latest_scrape_logs(
    db: Session = Depends(get_db_dep),
    _: models.User = Depends(get_admin_user_dep),
):
    return crud.get_latest_scrape_logs(db)
