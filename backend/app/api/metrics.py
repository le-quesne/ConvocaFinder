from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..services import crud
from .deps import get_db_dep

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("", response_model=schemas.MetricsResponse)
def get_metrics(db: Session = Depends(get_db_dep)):
    return crud.get_metrics(db)
