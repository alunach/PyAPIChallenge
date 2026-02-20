from __future__ import annotations

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"

class UserBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    role: UserRole = UserRole.user
    active: bool = True

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr | None = None
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    role: UserRole | None = None
    active: bool | None = None

class UserOut(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
