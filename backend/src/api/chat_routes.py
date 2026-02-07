from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
from typing import Optional
from pydantic import BaseModel
from ..database import get_session
from ..middleware.auth import get_current_user_id
from ..services.chat_service import ChatService


router = APIRouter(tags=["Chat"])


class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: list


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: Request,
    chat_request: ChatRequest,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Process chat message with AI agent and return assistant response
    Creates a new conversation if no conversation_id provided
    """

    # Input validation
    if not chat_request.message or len(chat_request.message.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content is required"
        )

    if len(chat_request.message) > 10000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content must be less than 10000 characters"
        )

    # Sanitize inputs - strip leading/trailing whitespace
    chat_request.message = chat_request.message.strip()

    # Process the chat request using the Chat Service
    result = ChatService.process_chat_message(
        session=session,
        user_id=int(current_user_id),
        conversation_id=chat_request.conversation_id,
        message=chat_request.message
    )

    return ChatResponse(
        conversation_id=result["conversation_id"],
        response=result["response"],
        tool_calls=result.get("tool_calls", [])
    )