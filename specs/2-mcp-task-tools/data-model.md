# Data Model: MCP Server & Task Tools

**Feature**: MCP Server & Task Tools
**Component**: Data Models
**Created**: 2026-01-22

## Entity Definitions

### Task Entity (Reused)
- **Purpose**: Represents a user task (reusing existing model)
- **Fields**:
  - `id`: Primary key, auto-generated integer
  - `user_id`: Foreign key linking to user who owns the task
  - `title`: Task title (1-255 characters)
  - `description`: Task description (nullable, 0-1000 characters)
  - `completed`: Boolean indicating task completion status
  - `created_at`: Timestamp when task was created
  - `updated_at`: Timestamp when task was last modified

### User Entity (Reused)
- **Purpose**: Represents authenticated users (reusing existing model)
- **Fields**:
  - `id`: Primary key, auto-generated integer
  - `username`: Unique username (1-100 characters)
  - `email`: Unique email address (5-255 characters)
  - `hashed_password`: Password hash
  - `is_active`: Boolean indicating if user is active
  - `created_at`: Timestamp when user was created
  - `updated_at`: Timestamp when user was last modified

### MCP Tool Parameters (New)
- **Purpose**: Defines parameter structures for each MCP tool
- **Fields**:
  - `user_id`: Required integer for all operations (enforces ownership)

## Relationships

- **One-to-Many**: One User can have many Tasks
- **Foreign Keys**:
  - Task.user_id references User.id

## Validation Rules

### Task Validation
- `user_id` must exist in User table
- `title` must be 1-255 characters
- `description` can be null or 0-1000 characters
- `completed` defaults to false

### MCP Tool Parameter Validation
- `user_id` must be a positive integer
- All required parameters must be provided for each tool
- Task IDs must exist in database for operations that require them

## Indexes

- Task: Index on `user_id` for efficient user-specific queries
- Task: Index on `completed` for efficient filtering
- User: Index on `email` for authentication lookups

## State Transitions

- **Task Completion**: `completed` field toggles between true/false
- **Task Updates**: `updated_at` field automatically updates on changes