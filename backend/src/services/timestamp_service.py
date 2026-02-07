from datetime import datetime
from sqlmodel import Session
from typing import TypeVar, Type, Any

T = TypeVar('T')

def update_model_updated_at(model_instance: T, session: Session) -> T:
    """
    Updates the updated_at field of a model instance before saving.

    Args:
        model_instance: The model instance to update
        session: The database session

    Returns:
        The updated model instance
    """
    if hasattr(model_instance, 'updated_at'):
        model_instance.updated_at = datetime.utcnow()

    session.add(model_instance)
    return model_instance


def prepare_model_for_update(model_instance: T) -> T:
    """
    Prepares a model instance for update by setting the updated_at field.

    Args:
        model_instance: The model instance to prepare for update

    Returns:
        The prepared model instance
    """
    if hasattr(model_instance, 'updated_at'):
        model_instance.updated_at = datetime.utcnow()
    return model_instance