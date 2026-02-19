import logging
import uuid
from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate

log = logging.getLogger("app.user_service")

class UserService:
    @staticmethod
    def create(db: Session, payload: UserCreate) -> User:
        user = User(
            username=payload.username,
            email=str(payload.email),
            first_name=payload.first_name,
            last_name=payload.last_name,
            role=payload.role.value,
            active=payload.active,
        )
        db.add(user)
        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()
            # Likely unique violation for username/email
            log.warning("integrity_error_on_create", error=str(e))
            raise
        db.refresh(user)
        return user

    @staticmethod
    def get(db: Session, user_id: uuid.UUID) -> Optional[User]:
        return db.get(User, user_id)

    @staticmethod
    def list(db: Session, active: Optional[bool] = None, limit: int = 100, offset: int = 0) -> Iterable[User]:
        stmt = select(User).order_by(User.created_at.desc()).limit(min(limit, 200)).offset(max(offset, 0))
        if active is not None:
            stmt = stmt.where(User.active == active)
        return db.execute(stmt).scalars().all()

    @staticmethod
    def update(db: Session, user: User, payload: UserUpdate) -> User:
        data = payload.model_dump(exclude_unset=True)
        if "email" in data and data["email"] is not None:
            data["email"] = str(data["email"])
        if "role" in data and data["role"] is not None:
            data["role"] = data["role"].value

        for k, v in data.items():
            setattr(user, k, v)

        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()
            log.warning("integrity_error_on_update", error=str(e))
            raise
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user: User) -> None:
        db.delete(user)
        db.commit()
