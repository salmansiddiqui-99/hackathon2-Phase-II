"""
AI Service Layer

This module provides a service layer that orchestrates the AI agent functionality
and integrates with other services like task management.
"""

from typing import Dict, Any, List, Optional
from sqlmodel import Session
from ..database import get_session
from ..models.conversation import Conversation
from ..models.message import Message
from ..mcp.tools import AddTaskParams, ListTasksParams, CompleteTaskParams, DeleteTaskParams, UpdateTaskParams
from ..mcp.server import get_mcp_server
from ..logging_config import logger
from ..ai.agent import get_ai_agent
from .chat_service import ChatService


class AIService:
    """
    Service class to handle AI-related operations with 9-step stateless conversation flow
    """

    # Constants for the 9-step conversation flow
    STEP_VALIDATE_INPUT = 1
    STEP_RETRIEVE_HISTORY = 2
    STEP_SAVE_USER_MESSAGE = 3
    STEP_PROCESS_WITH_AI = 4
    STEP_EXECUTE_TOOL_CALLS = 5
    STEP_GENERATE_FINAL_RESPONSE = 6
    STEP_SAVE_ASSISTANT_REPLY = 7
    STEP_UPDATE_CONVERSATION = 8
    STEP_RETURN_RESULT = 9

    @staticmethod
    def process_natural_language_request(
        user_id: int,
        message: str,
        conversation_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Process a natural language request using the AI agent with 9-step stateless flow.

        Args:
            user_id: The ID of the authenticated user
            message: The natural language message from the user
            conversation_id: Optional ID of an existing conversation

        Returns:
            Dictionary with AI response and any tool calls made
        """

        # Step 1: Validate input parameters
        logger.info(f"Step 1: Validating input for user {user_id}")
        if not message or len(message.strip()) == 0:
            return {
                "response": "Please provide a valid message to process.",
                "tool_calls": [],
                "tool_results": [],
                "error": "Empty message provided"
            }

        if len(message) > 10000:
            return {
                "response": "Message is too long. Please keep it under 10,000 characters.",
                "tool_calls": [],
                "tool_results": [],
                "error": "Message exceeds character limit"
            }

        # Sanitize message
        message = message.strip()

        # Step 2: Retrieve conversation history (if conversation_id provided)
        logger.info(f"Step 2: Retrieving conversation history for user {user_id}, conversation {conversation_id}")
        conversation_history = []
        if conversation_id:
            try:
                with next(get_session()) as session:
                    # Validate user access to conversation
                    if not ChatService.get_conversation_by_id(session, conversation_id, user_id):
                        return {
                            "response": "Access denied: Conversation not found or doesn't belong to you.",
                            "tool_calls": [],
                            "tool_results": [],
                            "error": "Conversation access violation"
                        }

                    conversation_history = AIService.get_conversation_history(session, conversation_id, user_id)
            except Exception as e:
                logger.error(f"Error retrieving conversation history: {str(e)}")
                return {
                    "response": f"Error retrieving conversation history: {str(e)}",
                    "tool_calls": [],
                    "tool_results": [],
                    "error": str(e)
                }

        # Step 3: Create or get conversation and save user message
        logger.info(f"Step 3: Creating/getting conversation and saving user message for user {user_id}")
        conversation = None
        user_message = None

        try:
            with next(get_session()) as session:
                # Create conversation if not provided
                if conversation_id is None:
                    conversation = ChatService.create_conversation(session, user_id)
                    conversation_id = conversation.id
                else:
                    conversation = ChatService.get_conversation_by_id(session, conversation_id, user_id)

                if not conversation:
                    return {
                        "response": "Failed to create/access conversation.",
                        "tool_calls": [],
                        "tool_results": [],
                        "error": "Conversation not found"
                    }

                # Save the user's message
                user_message = ChatService.save_message(
                    session=session,
                    conversation_id=conversation_id,
                    user_id=user_id,
                    role="user",
                    content=message
                )
        except Exception as e:
            logger.error(f"Error creating conversation or saving user message: {str(e)}")
            return {
                "response": f"Error creating conversation or saving message: {str(e)}",
                "tool_calls": [],
                "tool_results": [],
                "error": str(e)
            }

        # Step 4: Process the request with the AI agent
        logger.info(f"Step 4: Processing request with AI agent for user {user_id}")
        ai_agent = get_ai_agent()

        try:
            result = ai_agent.process_request(
                user_id=user_id,
                message=message,
                conversation_history=conversation_history
            )
        except Exception as e:
            logger.error(f"Error processing with AI agent: {str(e)}")
            return {
                "response": f"Error processing your request with the AI: {str(e)}",
                "tool_calls": [],
                "tool_results": [],
                "error": str(e)
            }

        # Step 5: Execute any tool calls if present (this is handled by the agent)
        # The agent already processes tool calls, so this step ensures proper handling

        # Step 6: Generate final response (already done by agent)
        response_content = result.get("response", "I processed your request but there was an issue generating a response.")
        tool_calls = result.get("tool_calls", [])
        tool_results = result.get("tool_results", [])

        # Step 7: Save the assistant's response
        logger.info(f"Step 7: Saving assistant response for user {user_id}")
        try:
            with next(get_session()) as session:
                # Verify conversation still exists and user has access
                conversation = ChatService.get_conversation_by_id(session, conversation_id, user_id)
                if not conversation:
                    logger.error(f"Conversation {conversation_id} not accessible for user {user_id}")
                    return {
                        "response": "Error: Conversation became inaccessible.",
                        "tool_calls": tool_calls,
                        "tool_results": tool_results,
                        "error": "Conversation access issue"
                    }

                # Save the assistant's response
                assistant_message = ChatService.save_message(
                    session=session,
                    conversation_id=conversation_id,
                    user_id=user_id,
                    role="assistant",
                    content=response_content
                )
        except Exception as e:
            logger.error(f"Error saving assistant response: {str(e)}")
            return {
                "response": f"Warning: Processed your request but couldn't save response: {str(e)}",
                "tool_calls": tool_calls,
                "tool_results": tool_results,
                "error": str(e)
            }

        # Step 8: Update conversation metadata
        logger.info(f"Step 8: Updating conversation metadata for {conversation_id}")
        try:
            with next(get_session()) as session:
                conversation = ChatService.get_conversation_by_id(session, conversation_id, user_id)
                if conversation:
                    from datetime import datetime
                    conversation.updated_at = datetime.utcnow()
                    session.add(conversation)
                    session.commit()
        except Exception as e:
            logger.error(f"Error updating conversation metadata: {str(e)}")
            # This is non-fatal, continue processing

        # Step 9: Return the final result
        logger.info(f"Step 9: Returning result for user {user_id}")
        return {
            "conversation_id": conversation_id,
            "response": response_content,
            "tool_calls": tool_calls
        }

    @staticmethod
    def validate_user_access_to_conversation(
        session: Session,
        user_id: int,
        conversation_id: int
    ) -> bool:
        """
        Validate that the user has access to the specified conversation.

        Args:
            session: Database session
            user_id: ID of the user requesting access
            conversation_id: ID of the conversation to validate

        Returns:
            bool: True if user has access, False otherwise
        """
        try:
            # Use ChatService for proper user isolation
            conversation = ChatService.get_conversation_by_id(session, conversation_id, user_id)
            return conversation is not None

        except Exception as e:
            logger.error(f"Error validating user access to conversation {conversation_id}: {str(e)}")
            return False

    @staticmethod
    def create_conversation_for_user(
        session: Session,
        user_id: int
    ) -> Conversation:
        """
        Create a new conversation for the specified user.

        Args:
            session: Database session
            user_id: ID of the user to create conversation for

        Returns:
            Conversation: The created conversation object
        """
        try:
            # Use ChatService for proper user isolation
            return ChatService.create_conversation(session, user_id)

        except Exception as e:
            logger.error(f"Error creating conversation for user {user_id}: {str(e)}")
            raise

    @staticmethod
    def save_message_to_conversation(
        session: Session,
        conversation_id: int,
        user_id: int,
        role: str,
        content: str
    ) -> Message:
        """
        Save a message to a conversation.

        Args:
            session: Database session
            conversation_id: ID of the conversation
            user_id: ID of the user who sent the message
            role: Role of the message sender ('user' or 'assistant')
            content: Content of the message

        Returns:
            Message: The saved message object
        """
        try:
            # Use ChatService for proper user isolation
            return ChatService.save_message(session, conversation_id, user_id, role, content)

        except Exception as e:
            logger.error(f"Error saving message to conversation {conversation_id}: {str(e)}")
            raise

    @staticmethod
    def get_conversation_history(
        session: Session,
        conversation_id: int,
        user_id: int
    ) -> List[Dict[str, str]]:
        """
        Get the conversation history for a specific conversation.

        Args:
            session: Database session
            conversation_id: ID of the conversation
            user_id: ID of the user requesting history

        Returns:
            List of messages in the conversation
        """
        try:
            # Use ChatService for proper user isolation
            messages = ChatService.get_conversation_history(session, conversation_id, user_id)

            # Format messages for the AI agent
            formatted_messages = []
            for msg in messages:
                formatted_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

            return formatted_messages

        except Exception as e:
            logger.error(f"Error getting conversation history for conversation {conversation_id}: {str(e)}")
            raise


# Global AI service instance
ai_service = AIService()