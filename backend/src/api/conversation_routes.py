from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional
from pydantic import BaseModel
from ..database import get_session
from ..middleware.auth import get_current_user_id
from ..services.chat_service import ChatService
from ..models.conversation import ConversationRead
from ..models.message import MessageRead

router = APIRouter(tags=["Conversations"])

class ConversationCreateRequest(BaseModel):
    pass  # Additional fields can be added here if needed


class MessageCreateRequest(BaseModel):
    conversation_id: int
    role: str
    content: str


class MessageUpdateRequest(BaseModel):
    content: str


@router.post("/conversations", response_model=ConversationRead)
def create_conversation(
    request: ConversationCreateRequest,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Create a new conversation for the authenticated user
    """
    user_id = int(current_user_id)

    conversation = ChatService.create_conversation(session, user_id)
    return conversation


@router.get("/conversations", response_model=List[ConversationRead])
def get_user_conversations(
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get all conversations for the authenticated user
    """
    user_id = int(current_user_id)

    conversations = ChatService.get_user_conversations(session, user_id)
    return conversations


@router.get("/conversations/{conversation_id}", response_model=ConversationRead)
def get_conversation(
    conversation_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get a specific conversation for the authenticated user
    """
    user_id = int(current_user_id)

    conversation = ChatService.get_conversation_by_id(session, conversation_id, user_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    return conversation


@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Delete a specific conversation for the authenticated user
    """
    user_id = int(current_user_id)

    success = ChatService.delete_conversation(session, conversation_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or does not belong to user"
        )

    return {"message": "Conversation deleted successfully"}


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageRead])
def get_conversation_messages(
    conversation_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get all messages in a specific conversation for the authenticated user
    """
    user_id = int(current_user_id)

    # First verify user has access to the conversation
    conversation = ChatService.get_conversation_by_id(session, conversation_id, user_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or does not belong to user"
        )

    messages = ChatService.get_conversation_history(session, conversation_id, user_id)
    return messages


@router.post("/messages", response_model=MessageRead)
def create_message(
    request: MessageCreateRequest,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Create a new message in a conversation for the authenticated user
    """
    user_id = int(current_user_id)

    # Verify user has access to the conversation
    conversation = ChatService.get_conversation_by_id(session, request.conversation_id, user_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or does not belong to user"
        )

    message = ChatService.save_message(
        session=session,
        conversation_id=request.conversation_id,
        user_id=user_id,
        role=request.role,
        content=request.content
    )
    return message


@router.get("/messages/{message_id}", response_model=MessageRead)
def get_message(
    message_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get a specific message for the authenticated user
    """
    user_id = int(current_user_id)

    message = ChatService.get_message_by_id(session, message_id, user_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found or does not belong to user"
        )

    return message


@router.put("/messages/{message_id}", response_model=MessageRead)
def update_message(
    message_id: int,
    request: MessageUpdateRequest,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Update a specific message for the authenticated user
    """
    user_id = int(current_user_id)

    message = ChatService.update_message(
        session=session,
        message_id=message_id,
        user_id=user_id,
        content=request.content
    )
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found or does not belong to user"
        )

    return message


@router.delete("/messages/{message_id}")
def delete_message(
    message_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Delete a specific message for the authenticated user
    """
    user_id = int(current_user_id)

    success = ChatService.delete_message(session, message_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found or does not belong to user"
        )

    return {"message": "Message deleted successfully"}