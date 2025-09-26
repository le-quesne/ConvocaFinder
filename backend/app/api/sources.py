from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, models
from ..services import crud
from .deps import get_admin_user_dep, get_db_dep

router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("", response_model=list[schemas.SourceRead])
def list_sources(db: Session = Depends(get_db_dep)):
    return crud.list_sources(db)


@router.post("", response_model=schemas.SourceRead)
def create_source(
    source_in: schemas.SourceBase,
    db: Session = Depends(get_db_dep),
    _: models.User = Depends(get_admin_user_dep),
):
    return crud.create_source(db, source_in)
