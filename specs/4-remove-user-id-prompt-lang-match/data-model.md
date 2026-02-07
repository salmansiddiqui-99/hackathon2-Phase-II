# Data Model: Remove explicit User ID prompting and add automatic multi-language response matching

## Overview
This document describes the data entities and models involved in the implementation of seamless user ID handling and automatic language response matching for the AI Todo Chatbot.

## Entity: Task
**Description**: Represents a user's task with properties and relationships to the authenticated user.

**Fields**:
- id: Integer (primary key, auto-generated)
- title: String (required, max 255 characters)
- description: String (optional, max 1000 characters)
- completed: Boolean (default false)
- created_at: DateTime (auto-populated)
- updated_at: DateTime (auto-populated)
- user_id: Integer (foreign key to User, automatically populated from JWT)

**Relationships**:
- Belongs to one User (via user_id foreign key)
- Each user can have multiple tasks

**Validation Rules**:
- Title must be present and not empty
- Title must be less than 255 characters
- Description must be less than 1000 characters if provided
- user_id must match the authenticated user from JWT token

## Entity: User
**Description**: Represents an authenticated user in the system.

**Fields**:
- id: Integer (primary key, auto-generated)
- email: String (unique, required)
- hashed_password: String (required, stored securely)
- created_at: DateTime (auto-populated)
- updated_at: DateTime (auto-populated)

**State Transitions**:
- Unauthenticated → Authenticated (via login)
- Authenticated → Logged out (via logout)

## Entity: Conversation
**Description**: Represents a conversation thread between user and AI assistant.

**Fields**:
- id: Integer (primary key, auto-generated)
- user_id: Integer (foreign key to User)
- created_at: DateTime (auto-populated)
- updated_at: DateTime (auto-populated)

**Relationships**:
- Belongs to one User
- Contains multiple Messages

## Entity: Message
**Description**: Represents a message in a conversation.

**Fields**:
- id: Integer (primary key, auto-generated)
- conversation_id: Integer (foreign key to Conversation)
- role: String (either 'user' or 'assistant')
- content: Text (the message content)
- timestamp: DateTime (auto-populated)

**Relationships**:
- Belongs to one Conversation
- Part of a conversation thread

## Data Flow
1. User authenticates and receives JWT token
2. User sends message to chat endpoint with JWT in headers
3. Server decodes JWT to extract user_id
4. User ID is automatically associated with all task operations
5. AI agent responds in the same language as the user's input
6. All data access is filtered by the authenticated user_id

## Security Constraints
- All data access is limited to the authenticated user's records
- User_id is extracted from JWT token, never from user input
- Tasks created/updated/deleted are always associated with the authenticated user