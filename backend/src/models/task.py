from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from .base import TimestampMixin


class TaskBase(SQLModel):
    """Base model for Task with common fields"""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Task(TaskBase, TimestampMixin, table=True):
    """Task model for database storage"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)  # Foreign key to user


class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    pass


class TaskRead(TaskBase):
    """Schema for reading a task with its ID"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    """Schema for updating an existing task"""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None