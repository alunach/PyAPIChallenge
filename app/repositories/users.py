from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.models import User

class UsersRepository:
    def create(self, db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def list(self, db: Session, *, active: bool | None, limit: int, offset: int) -> list[User]:
        stmt = select(User).order_by(User.created_at.desc()).limit(limit).offset(offset)
        if active is not None:
            stmt = stmt.where(User.active == active)
        return list(db.execute(stmt).scalars().all())

    def get(self, db: Session, user_id: str) -> User | None:
        return db.get(User, user_id)

    def get_by_username(self, db: Session, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return db.execute(stmt).scalars().first()

    def get_by_email(self, db: Session, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return db.execute(stmt).scalars().first()

    def update(self, db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
