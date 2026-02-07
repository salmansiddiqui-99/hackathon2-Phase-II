from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from .base import TimestampMixin
from ..auth import get_password_hash


class UserBase(SQLModel):
    """Base model for User with common fields"""
    username: str = Field(min_length=1, max_length=100)
    email: str = Field(unique=True, min_length=5, max_length=255)


class User(UserBase, TimestampMixin, table=True):
    """User model for database storage"""
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(min_length=1)
    is_active: bool = Field(default=True)

    def set_password(self, password: str):
        """Hash and set the user's password"""
        self.hashed_password = get_password_hash(password)


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str


class UserRead(UserBase):
    """Schema for reading a user with its ID"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserLogin(SQLModel):
    """Schema for user login"""
    email: str
    password: str