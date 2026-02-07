from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class TimestampMixin:
    """
    Mixin class to add created_at and updated_at timestamp fields to models.
    Note: For automatic updated_at updates, service layer logic should handle this.
    """
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)