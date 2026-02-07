# Data Model: Natural Task Reference by Title

## Overview
This document describes the data entities and models involved in the implementation of natural task reference by title for the AI Todo Chatbot. The implementation primarily affects how the AI agent processes and resolves task references, while maintaining the underlying data structure.

## Entity: Task
**Description**: Represents a user's task with properties and relationships to the authenticated user.

**Fields**:
- id: Integer (primary key, auto-generated, internal use only)
- title: String (required, max 255 characters, user-facing)
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

**Access Patterns**:
- Primary access by task ID for MCP tools
- Secondary access by title matching (for user interaction)
- User access restricted to their own tasks only

## Entity: User
**Description**: Represents an authenticated user in the system.

**Fields**:
- id: Integer (primary key, auto-generated)
- email: String (unique, required)
- hashed_password: String (required, stored securely)
- created_at: DateTime (auto-populated)
- updated_at: DateTime (auto-populated)

**Relationships**:
- Has many Tasks
- Has many Conversations

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

## Data Flow for Title Resolution
1. User sends message: "complete my task buy groceries"
2. AI agent recognizes title-based command
3. Agent internally calls list_tasks API to retrieve user's tasks
4. Agent performs fuzzy matching between "buy groceries" and retrieved task titles
5. If unique match found (e.g., task with title "buy groceries"):
   - Agent extracts the task ID (e.g., ID 123)
   - Agent calls complete_task API with task ID 123
6. If multiple matches found (e.g., "buy groceries" and "buy groceries for party"):
   - Agent responds with clarification: "I found two tasks with similar titles: 1. buy groceries 2. buy groceries for party. Which one do you mean?"
7. If no match found:
   - Agent responds: "I couldn't find a task called 'buy groceries'. Here are your tasks: [...]"
8. User confirms selection, and process continues

## Security Constraints
- All data access is limited to the authenticated user's records
- Task IDs are internal identifiers and not exposed to users
- Title matching only operates within the authenticated user's task set
- No cross-user task access is possible through title matching