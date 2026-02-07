# Data Model: Chat Database & Stateless Endpoint

**Feature**: Chat Database & Stateless Endpoint
**Component**: Data Models
**Created**: 2026-01-21

## Entity Definitions

### Conversation Entity
- **Purpose**: Represents a chat conversation thread
- **Fields**:
  - `id`: Primary key, auto-generated integer
  - `user_id`: Foreign key linking to user who owns the conversation
  - `created_at`: Timestamp when conversation was initiated
  - `updated_at`: Timestamp when conversation was last modified

### Message Entity
- **Purpose**: Represents individual messages within conversations
- **Fields**:
  - `id`: Primary key, auto-generated integer
  - `conversation_id`: Foreign key linking to parent conversation
  - `user_id`: Foreign key linking to user who sent the message
  - `role`: String indicating sender type ("user" or "assistant")
  - `content`: Text content of the message
  - `timestamp`: When the message was created

## Relationships

- **One-to-Many**: One Conversation can have many Messages
- **Foreign Keys**:
  - Message.user_id references User.id
  - Message.conversation_id references Conversation.id
  - Conversation.user_id references User.id

## Validation Rules

### Conversation Validation
- `user_id` must exist in User table
- `created_at` and `updated_at` automatically set by system

### Message Validation
- `conversation_id` must exist in Conversation table
- `user_id` must exist in User table
- `role` must be either "user" or "assistant"
- `content` must be 1-10000 characters
- `timestamp` automatically set by system

## Indexes

- Conversation: Index on `user_id` for efficient user-specific queries
- Message: Index on `conversation_id` and `user_id` for efficient filtering
- Message: Index on `timestamp` for chronological ordering

## State Transitions

- **Conversation**: Created when first message is sent without conversation_id
- **Message**: Created when user sends message or assistant responds