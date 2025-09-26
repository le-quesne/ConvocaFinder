from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import schemas
from ..services import crud
from ..auth import security
from .deps import get_db_dep

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db_dep)):
    existing = security.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    user = crud.create_user(db, user_in)
    return user


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_dep)):
    user = security.authenticate_user(db, form_data.username, form_data.password)
    token = security.create_access_token({"sub": user.email})
    return schemas.Token(access_token=token)
