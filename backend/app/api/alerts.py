from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, models
from ..services import crud
from .deps import get_current_user_dep, get_db_dep

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.post("", response_model=schemas.AlertRead)
def create_alert(
    alert_in: schemas.AlertCreate,
    db: Session = Depends(get_db_dep),
    current_user: models.User = Depends(get_current_user_dep),
):
    alert = crud.create_alert(db, current_user, alert_in)
    return alert
