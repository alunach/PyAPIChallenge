from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models import User
from app.repositories.users import UsersRepository
from app.schemas.users import UserCreate, UserUpdate

class UsersService:
    def __init__(self, repo: UsersRepository | None = None):
        self.repo = repo or UsersRepository()

    def create_user(self, db: Session, payload: UserCreate) -> User:
        # Uniqueness checks -> 409
        if self.repo.get_by_username(db, payload.username):
            raise ValueError("username_exists")
        if self.repo.get_by_email(db, str(payload.email)):
            raise ValueError("email_exists")

        user = User(
            username=payload.username,
            email=str(payload.email),
            first_name=payload.first_name,
            last_name=payload.last_name,
            role=payload.role.value,
            active=payload.active,
        )
        return self.repo.create(db, user)

    def list_users(self, db: Session, *, active: bool | None, limit: int, offset: int) -> list[User]:
        return self.repo.list(db, active=active, limit=limit, offset=offset)

    def get_user(self, db: Session, user_id: str) -> User | None:
        return self.repo.get(db, user_id)

    def update_user(self, db: Session, user_id: str, payload: UserUpdate) -> User | None:
        user = self.repo.get(db, user_id)
        if not user:
            return None

        # Email uniqueness if changing
        if payload.email is not None and str(payload.email) != user.email:
            if self.repo.get_by_email(db, str(payload.email)):
                raise ValueError("email_exists")
            user.email = str(payload.email)

        if payload.first_name is not None:
            user.first_name = payload.first_name
        if payload.last_name is not None:
            user.last_name = payload.last_name
        if payload.role is not None:
            user.role = payload.role.value
        if payload.active is not None:
            user.active = payload.active

        return self.repo.update(db, user)

    def soft_delete_user(self, db: Session, user_id: str) -> bool:
        user = self.repo.get(db, user_id)
        if not user:
            return False
        user.active = False
        self.repo.update(db, user)
        return True
