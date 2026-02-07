from sqlmodel import Session, select
from typing import Dict, Any, Optional
from datetime import datetime
import uuid  # For generating simple responses in the meantime
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message, MessageCreate
from ..logging_config import logger


class ChatService:
    @staticmethod
    def create_conversation(session: Session, user_id: int) -> Conversation:
        """
        Create a new conversation for the user
        """
        logger.info(f"Creating new conversation for user_id: {user_id}")
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        logger.info(f"Created conversation with id: {conversation.id} for user_id: {user_id}")
        return conversation

    @staticmethod
    def get_conversation_by_id(session: Session, conversation_id: int, user_id: int) -> Optional[Conversation]:
        """
        Get a specific conversation by ID for the user (enforcing user isolation)
        """
        logger.info(f"Fetching conversation {conversation_id} for user_id: {user_id}")
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = session.exec(statement).first()
        if conversation:
            logger.info(f"Found conversation {conversation_id} for user_id: {user_id}")
        else:
            logger.warning(f"Conversation {conversation_id} not found for user_id: {user_id}")
        return conversation

    @staticmethod
    def save_message(session: Session, conversation_id: int, user_id: int, role: str, content: str) -> Message:
        """
        Save a message to the conversation
        """
        logger.info(f"Saving {role} message to conversation {conversation_id} for user_id: {user_id}")
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        logger.info(f"Saved message with id: {message.id} to conversation {conversation_id}")
        return message

    @staticmethod
    def get_conversation_history(session: Session, conversation_id: int, user_id: int) -> list:
        """
        Get all messages in a conversation, enforcing user isolation
        """
        logger.info(f"Fetching conversation history for conversation {conversation_id} and user_id: {user_id}")
        statement = select(Message).where(
            Message.conversation_id == conversation_id,
            Message.user_id == user_id
        ).order_by(Message.timestamp)
        messages = session.exec(statement).all()
        logger.info(f"Retrieved {len(messages)} messages from conversation {conversation_id}")
        return messages

    @staticmethod
    def process_chat_message(session: Session, user_id: int, conversation_id: Optional[int], message: str) -> Dict[str, Any]:
        """
        Process a chat message, creating or continuing a conversation
        """
        logger.info(f"Processing chat message for user_id: {user_id}, conversation_id: {conversation_id}")

        # If no conversation_id is provided, create a new conversation
        if conversation_id is None:
            logger.info(f"No conversation_id provided, creating new conversation for user_id: {user_id}")
            conversation = ChatService.create_conversation(session, user_id)
            conversation_id = conversation.id
        else:
            # Verify the conversation belongs to the user
            conversation = ChatService.get_conversation_by_id(session, conversation_id, user_id)
            if not conversation:
                logger.error(f"Conversation {conversation_id} not found or does not belong to user {user_id}")
                raise ValueError("Conversation not found or does not belong to user")

        # Fetch the conversation history to provide context (stateless approach)
        conversation_history = ChatService.get_conversation_history(session, conversation_id, user_id)

        # Save the user's message
        user_message = ChatService.save_message(
            session=session,
            conversation_id=conversation_id,
            user_id=user_id,
            role="user",
            content=message
        )

        # Process the message using the AI service
        try:
            # Import ai_service locally to avoid circular import
            from ..services.ai_service import ai_service

            # Format conversation history for the AI agent
            formatted_history = []
            for msg in conversation_history:
                formatted_history.append({
                    "role": msg.role,
                    "content": msg.content
                })

            # Process the request with the AI agent through the AI service
            ai_result = ai_service.process_natural_language_request(
                user_id=user_id,
                message=message,
                conversation_id=conversation_id
            )

            response_content = ai_result.get("response", "I processed your request but there was an issue generating a response.")
            tool_calls = ai_result.get("tool_calls", [])
            tool_results = ai_result.get("tool_results", [])

        except ImportError as e:
            logger.error(f"Error importing AI service: {str(e)}")
            response_content = "Sorry, there was an issue with the AI service configuration."
            tool_calls = []
            tool_results = []
        except Exception as e:
            logger.error(f"Error processing message with AI agent: {str(e)}")
            response_content = f"Sorry, I encountered an error processing your request: {str(e)}"
            tool_calls = []
            tool_results = []

        # Save the assistant's response
        assistant_message = ChatService.save_message(
            session=session,
            conversation_id=conversation_id,
            user_id=user_id,  # The assistant acts on behalf of the user in this context
            role="assistant",
            content=response_content
        )

        # Update the conversation's updated_at timestamp
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()

        logger.info(f"Successfully processed chat message for conversation {conversation_id}")

        return {
            "conversation_id": conversation_id,
            "response": response_content,
            "tool_calls": tool_calls
        }

    @staticmethod
    def get_user_conversations(session: Session, user_id: int) -> list:
        """
        Get all conversations for a specific user (enforcing user isolation)
        """
        logger.info(f"Fetching all conversations for user_id: {user_id}")
        statement = select(Conversation).where(
            Conversation.user_id == user_id
        ).order_by(Conversation.created_at.desc())
        conversations = session.exec(statement).all()
        logger.info(f"Retrieved {len(conversations)} conversations for user_id: {user_id}")
        return conversations

    @staticmethod
    def delete_conversation(session: Session, conversation_id: int, user_id: int) -> bool:
        """
        Delete a specific conversation for the user (enforcing user isolation)
        """
        logger.info(f"Deleting conversation {conversation_id} for user_id: {user_id}")
        conversation = ChatService.get_conversation_by_id(session, conversation_id, user_id)
        if not conversation:
            logger.warning(f"Cannot delete conversation {conversation_id} - not found or doesn't belong to user {user_id}")
            return False

        session.delete(conversation)
        session.commit()
        logger.info(f"Deleted conversation {conversation_id} for user_id: {user_id}")
        return True

    @staticmethod
    def get_message_by_id(session: Session, message_id: int, user_id: int) -> Optional[Message]:
        """
        Get a specific message by ID for the user (enforcing user isolation)
        """
        logger.info(f"Fetching message {message_id} for user_id: {user_id}")
        statement = select(Message).where(
            Message.id == message_id,
            Message.user_id == user_id
        )
        message = session.exec(statement).first()
        if message:
            logger.info(f"Found message {message_id} for user_id: {user_id}")
        else:
            logger.warning(f"Message {message_id} not found for user_id: {user_id}")
        return message

    @staticmethod
    def update_message(session: Session, message_id: int, user_id: int, content: str) -> Optional[Message]:
        """
        Update a specific message for the user (enforcing user isolation)
        """
        logger.info(f"Updating message {message_id} for user_id: {user_id}")
        message = ChatService.get_message_by_id(session, message_id, user_id)
        if not message:
            logger.warning(f"Cannot update message {message_id} - not found or doesn't belong to user {user_id}")
            return None

        message.content = content
        message.updated_at = datetime.utcnow()
        session.add(message)
        session.commit()
        session.refresh(message)
        logger.info(f"Updated message {message_id} for user_id: {user_id}")
        return message

    @staticmethod
    def delete_message(session: Session, message_id: int, user_id: int) -> bool:
        """
        Delete a specific message for the user (enforcing user isolation)
        """
        logger.info(f"Deleting message {message_id} for user_id: {user_id}")
        message = ChatService.get_message_by_id(session, message_id, user_id)
        if not message:
            logger.warning(f"Cannot delete message {message_id} - not found or doesn't belong to user {user_id}")
            return False

        session.delete(message)
        session.commit()
        logger.info(f"Deleted message {message_id} for user_id: {user_id}")
        return True