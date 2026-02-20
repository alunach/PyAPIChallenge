from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.users import UserCreate, UserOut, UserUpdate
from app.services.users import UsersService

router = APIRouter(prefix="/users", tags=["Users"])

def get_service() -> UsersService:
    return UsersService()

@router.post(
    "",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"description": "Username or email already exists"},
        422: {"description": "Validation error"},
    },
)
def create_user(payload: UserCreate, db: Session = Depends(get_db), svc: UsersService = Depends(get_service)):
    try:
        user = svc.create_user(db, payload)
        return _to_out(user)
    except ValueError as e:
        if str(e) in {"username_exists", "email_exists"}:
            raise HTTPException(status_code=409, detail=str(e))
        raise

@router.get("", response_model=list[UserOut])
def list_users(
    db: Session = Depends(get_db),
    svc: UsersService = Depends(get_service),
    active: bool | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    users = svc.list_users(db, active=active, limit=limit, offset=offset)
    return [_to_out(u) for u in users]

@router.get("/{user_id}", response_model=UserOut, responses={404: {"description": "Not found"}})
def get_user(user_id: str, db: Session = Depends(get_db), svc: UsersService = Depends(get_service)):
    user = svc.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _to_out(user)

@router.put("/{user_id}", response_model=UserOut, responses={404: {"description": "Not found"}, 409: {"description": "Email already exists"}})
def update_user(user_id: str, payload: UserUpdate, db: Session = Depends(get_db), svc: UsersService = Depends(get_service)):
    try:
        user = svc.update_user(db, user_id, payload)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return _to_out(user)
    except ValueError as e:
        if str(e) == "email_exists":
            raise HTTPException(status_code=409, detail="email_exists")
        raise

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"description": "Not found"}})
def delete_user(user_id: str, db: Session = Depends(get_db), svc: UsersService = Depends(get_service)):
    ok = svc.soft_delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return None

def _to_out(user) -> UserOut:
    # role stored as string in DB
    return UserOut(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        created_at=user.created_at,
        updated_at=user.updated_at,
        active=user.active,
    )
