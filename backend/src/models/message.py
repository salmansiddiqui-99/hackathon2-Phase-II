from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from .base import TimestampMixin


class MessageBase(SQLModel):
    """Base model for Message with common fields"""
    conversation_id: int = Field(index=True)  # Foreign key to conversation
    user_id: int = Field(index=True)  # Foreign key to user
    role: str = Field(regex="^(user|assistant)$", max_length=20)  # user or assistant
    content: str = Field(min_length=1, max_length=10000)  # Message content


class Message(MessageBase, TimestampMixin, table=True):
    """Message model for database storage"""
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)


class MessageCreate(MessageBase):
    """Schema for creating a new message"""
    pass


class MessageRead(MessageBase):
    """Schema for reading a message with its ID"""
    id: int
    timestamp: datetime
    created_at: datetime
    updated_at: datetime