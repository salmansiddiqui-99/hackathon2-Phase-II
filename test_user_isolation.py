"""
Test script to verify user isolation in chatbot functionality.
This script tests that users can only access their own conversations and messages.
"""

import asyncio
import tempfile
import os
from sqlmodel import Session, SQLModel, create_engine
from backend.src.models.conversation import Conversation
from backend.src.models.message import Message
from backend.src.services.chat_service import ChatService

def test_user_isolation():
    """Test that users can only access their own data"""

    # Create a temporary database for testing
    temp_db_fd, temp_db_path = tempfile.mkstemp(suffix='.db')
    temp_db_url = f"sqlite:///{temp_db_path}"

    # Create test database
    engine = create_engine(temp_db_url, echo=False)  # Disable SQL logging for cleaner output
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Create test users
        user1_id = 1
        user2_id = 2

        # Create conversations for user 1
        conv1_user1 = ChatService.create_conversation(session, user1_id)
        conv2_user1 = ChatService.create_conversation(session, user1_id)

        # Create conversations for user 2
        conv1_user2 = ChatService.create_conversation(session, user2_id)
        conv2_user2 = ChatService.create_conversation(session, user2_id)

        # Add messages to user 1's conversations
        msg1_conv1_user1 = ChatService.save_message(
            session, conv1_user1.id, user1_id, "user", "Hello from user 1"
        )
        msg2_conv1_user1 = ChatService.save_message(
            session, conv1_user1.id, user1_id, "assistant", "Hi back to user 1"
        )

        # Add messages to user 2's conversations
        msg1_conv1_user2 = ChatService.save_message(
            session, conv1_user2.id, user2_id, "user", "Hello from user 2"
        )
        msg2_conv1_user2 = ChatService.save_message(
            session, conv1_user2.id, user2_id, "assistant", "Hi back to user 2"
        )

        print("=== Testing User Isolation ===")

        # Test 1: User 1 should be able to access their own conversations
        user1_conversations = ChatService.get_user_conversations(session, user1_id)
        print(f"User 1 has {len(user1_conversations)} conversations (should be 2)")
        assert len(user1_conversations) == 2, f"Expected 2 conversations for user 1, got {len(user1_conversations)}"

        # Test 2: User 2 should be able to access their own conversations
        user2_conversations = ChatService.get_user_conversations(session, user2_id)
        print(f"User 2 has {len(user2_conversations)} conversations (should be 2)")
        assert len(user2_conversations) == 2, f"Expected 2 conversations for user 2, got {len(user2_conversations)}"

        # Test 3: User 1 should NOT be able to access user 2's conversations
        user2_conv_for_user1 = ChatService.get_conversation_by_id(session, conv1_user2.id, user1_id)
        print(f"User 1 trying to access user 2's conversation: {user2_conv_for_user1 is None} (should be True)")
        assert user2_conv_for_user1 is None, "User 1 should not be able to access user 2's conversation"

        # Test 4: User 2 should NOT be able to access user 1's conversations
        user1_conv_for_user2 = ChatService.get_conversation_by_id(session, conv1_user1.id, user2_id)
        print(f"User 2 trying to access user 1's conversation: {user1_conv_for_user2 is None} (should be True)")
        assert user1_conv_for_user2 is None, "User 2 should not be able to access user 1's conversation"

        # Test 5: User 1 should be able to access their own messages
        conv1_user1_messages = ChatService.get_conversation_history(session, conv1_user1.id, user1_id)
        print(f"User 1 messages in their conversation: {len(conv1_user1_messages)} (should be 2)")
        assert len(conv1_user1_messages) == 2, f"Expected 2 messages for user 1 in their conversation, got {len(conv1_user1_messages)}"

        # Test 6: User 2 should NOT be able to access user 1's messages in that conversation
        conv1_user1_messages_for_user2 = ChatService.get_conversation_history(session, conv1_user1.id, user2_id)
        print(f"User 2 trying to access user 1's messages: {len(conv1_user1_messages_for_user2)} (should be 0)")
        assert len(conv1_user1_messages_for_user2) == 0, f"User 2 should not be able to access user 1's messages, got {len(conv1_user1_messages_for_user2)}"

        # Test 7: Test message-level access control
        msg_from_user2_for_user1 = ChatService.get_message_by_id(session, msg1_conv1_user2.id, user1_id)
        print(f"User 1 trying to access user 2's message: {msg_from_user2_for_user1 is None} (should be True)")
        assert msg_from_user2_for_user1 is None, "User 1 should not be able to access user 2's message"

        msg_from_user1_for_user1 = ChatService.get_message_by_id(session, msg1_conv1_user1.id, user1_id)
        print(f"User 1 accessing their own message: {msg_from_user1_for_user1 is not None} (should be True)")
        assert msg_from_user1_for_user1 is not None, "User 1 should be able to access their own message"

        # Test 8: Test deletion permissions
        # User 1 should not be able to delete user 2's conversation
        delete_result = ChatService.delete_conversation(session, conv1_user2.id, user1_id)
        print(f"User 1 trying to delete user 2's conversation: {not delete_result} (should be True)")
        assert not delete_result, "User 1 should not be able to delete user 2's conversation"

        # User 1 should be able to delete their own conversation
        delete_result = ChatService.delete_conversation(session, conv2_user1.id, user1_id)
        print(f"User 1 deleting their own conversation: {delete_result} (should be True)")
        assert delete_result, "User 1 should be able to delete their own conversation"

        print("\n=== All User Isolation Tests Passed! ===")
        print("[PASS] Users can only access their own conversations")
        print("[PASS] Users can only access their own messages")
        print("[PASS] Users cannot access other users' data")
        print("[PASS] Proper filtering is enforced at the database level")

    # Clean up the temporary database file
    try:
        os.close(temp_db_fd)
        os.unlink(temp_db_path)
    except PermissionError:
        # On Windows, the file might still be locked, so we'll just log and continue
        print(f"Warning: Could not delete temporary database file {temp_db_path}. This is common on Windows.")
        pass


if __name__ == "__main__":
    test_user_isolation()