from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from .base import TimestampMixin


class ConversationBase(SQLModel):
    """Base model for Conversation with common fields"""
    user_id: int = Field(index=True)  # Foreign key to user


class Conversation(ConversationBase, TimestampMixin, table=True):
    """Conversation model for database storage"""
    id: Optional[int] = Field(default=None, primary_key=True)


class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation"""
    pass


class ConversationRead(ConversationBase):
    """Schema for reading a conversation with its ID"""
    id: int
    created_at: datetime
    updated_at: datetime