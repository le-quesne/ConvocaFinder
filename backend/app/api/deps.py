from fastapi import Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..auth.security import get_current_active_user, get_current_admin_user
from .. import models


def get_current_user_dep(current_user: models.User = Depends(get_current_active_user)) -> models.User:
    return current_user


def get_admin_user_dep(current_user: models.User = Depends(get_current_admin_user)) -> models.User:
    return current_user


def get_db_dep(db: Session = Depends(get_db)) -> Session:
    return db
