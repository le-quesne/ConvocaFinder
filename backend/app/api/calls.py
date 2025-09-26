from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import schemas, models
from ..services import crud
from .deps import get_current_user_dep, get_db_dep

router = APIRouter(prefix="/convocatorias", tags=["convocatorias"])


@router.get("", response_model=schemas.PaginatedCalls)
def list_calls(
    db: Session = Depends(get_db_dep),
    country: str | None = Query(None),
    funding_type: str | None = Query(None),
    amount_min: float | None = Query(None, ge=0),
    amount_max: float | None = Query(None, ge=0),
    closing_before: date | None = Query(None),
    closing_after: date | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    filters = schemas.CallFilter(
        country=country,
        funding_type=funding_type,
        amount_min=amount_min,
        amount_max=amount_max,
        closing_before=closing_before,
        closing_after=closing_after,
    )
    calls, total = crud.get_calls(db, filters, page, size)
    return schemas.PaginatedCalls(
        data=calls,
        pagination=schemas.Pagination(total=total, page=page, size=size),
    )


@router.get("/{call_id}", response_model=schemas.CallRead)
def get_call(call_id: int, db: Session = Depends(get_db_dep)):
    call = crud.get_call(db, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")
    return call


@router.post("/{call_id}/favorite", response_model=schemas.FavoriteRead)
def favorite_call(
    call_id: int,
    db: Session = Depends(get_db_dep),
    current_user: models.User = Depends(get_current_user_dep),
):
    call = crud.get_call(db, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")
    favorite = crud.add_favorite(db, current_user, call)
    return favorite
