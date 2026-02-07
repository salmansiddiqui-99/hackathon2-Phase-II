# Quickstart Guide: Chat Database & Stateless Endpoint

## Overview
This guide outlines the implementation of the chat database and stateless endpoint feature, including Conversation and Message models, chat API endpoint, and stateless processing.

## Prerequisites
- Backend running with existing user authentication
- Neon PostgreSQL database configured
- BETTER_AUTH_SECRET environment variable set

## Implementation Steps

### 1. Database Models
Create the Conversation and Message models in `backend/src/models/`:

1. Create `conversation.py` with Conversation SQLModel
2. Create `message.py` with Message SQLModel
3. Define relationships between models
4. Add proper indexes for performance

### 2. Service Layer
Create ChatService in `backend/src/services/`:

1. Implement conversation creation/retrieval
2. Implement message history loading
3. Implement message persistence logic
4. Ensure stateless operation (no server-side storage)

### 3. API Endpoint
Create chat endpoint in `backend/src/api/`:

1. Create `chat_routes.py` with POST /api/{user_id}/chat
2. Integrate JWT authentication using existing middleware
3. Validate user_id matches authenticated user
4. Handle optional conversation_id parameter

### 4. Integration
Connect components in the main application:

1. Import and register chat router in `backend/src/api/__init__.py`
2. Update main application in `backend/src/main.py`
3. Ensure backward compatibility with existing endpoints

## Configuration
- Ensure DATABASE_URL points to Neon PostgreSQL
- Verify BETTER_AUTH_SECRET is properly set
- Confirm JWT middleware is active

## Testing
1. Test new conversation creation: POST without conversation_id
2. Test conversation continuation: POST with existing conversation_id
3. Test user isolation: Verify users can't access others' conversations
4. Test authentication: Verify 401 for invalid/missing tokens
5. Test stateless operation: Multiple requests should work consistently