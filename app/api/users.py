import logging
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])
log = logging.getLogger("app.users_api")

def _conflict(detail: str):
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        return UserService.create(db, payload)
    except IntegrityError:
        _conflict("username or email already exists")

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = UserService.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("", response_model=list[UserOut])
def list_users(
    active: bool | None = Query(default=None, description="Filter by active flag"),
    limit: int = Query(default=100, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    return UserService.list(db, active=active, limit=limit, offset=offset)

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: uuid.UUID, payload: UserUpdate, db: Session = Depends(get_db)):
    user = UserService.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        return UserService.update(db, user, payload)
    except IntegrityError:
        _conflict("username or email already exists")

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = UserService.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    UserService.delete(db, user)
    return None
