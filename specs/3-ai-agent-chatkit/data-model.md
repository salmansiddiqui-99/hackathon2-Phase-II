# Data Model: AI Agent & ChatKit Integration

**Feature**: AI Agent & ChatKit Integration
**Component**: Data Models
**Created**: 2026-01-22

## Entity Definitions

### AI Agent Request Entity
- **Purpose**: Represents a natural language request from the user to the AI agent
- **Fields**:
  - `conversation_id`: Optional string identifier for conversation continuity
  - `user_id`: Integer identifier for the authenticated user
  - `message`: String containing the natural language query/command
  - `timestamp`: DateTime when the request was made

### AI Agent Response Entity
- **Purpose**: Represents the AI agent's response to a user request
- **Fields**:
  - `conversation_id`: String identifier for the conversation
  - `response`: String containing the AI's natural language response
  - `tool_calls`: Array of objects representing tools called by the AI
  - `timestamp`: DateTime when the response was generated

### Tool Call Entity
- **Purpose**: Represents a specific tool call made by the AI agent
- **Fields**:
  - `tool_name`: String name of the tool called (e.g., "add_task", "list_tasks")
  - `arguments`: Object containing the arguments passed to the tool
  - `result`: Object containing the result returned by the tool
  - `timestamp`: DateTime when the tool was called

### OpenRouter Configuration Entity
- **Purpose**: Represents the configuration for OpenRouter API access
- **Fields**:
  - `api_key`: String containing the OpenRouter API key
  - `model`: String specifying the model to use (tngtech/deepseek-r1t2-chimera:free)
  - `base_url`: String containing the OpenRouter API base URL
  - `temperature`: Float for controlling response randomness (optional)

## Relationships

- **One-to-Many**: One conversation can have many AI Agent Requests and Responses
- **Request-Response**: Each AI Agent Request corresponds to one AI Agent Response
- **Response-ToolCalls**: One AI Agent Response can trigger multiple Tool Calls

## Validation Rules

### AI Agent Request Validation
- `user_id` must be a positive integer (validated via existing JWT authentication)
- `message` must be 1-10000 characters
- `conversation_id` must be a valid UUID format if provided

### Tool Call Validation
- `tool_name` must be one of the valid MCP tools: "add_task", "list_tasks", "complete_task", "delete_task", "update_task"
- `arguments` must match the expected schema for the specific tool
- `result` must conform to the expected return format for the tool

### OpenRouter Configuration Validation
- `api_key` must be a valid OpenRouter API key format
- `model` must be a supported model identifier
- `base_url` must be a valid HTTPS URL

## Indexes

- AI Agent Request: Index on `user_id` and `conversation_id` for efficient user-specific queries
- AI Agent Response: Index on `conversation_id` for chronological ordering
- Tool Call: Index on `tool_name` for efficient tool usage analytics

## State Transitions

- **Conversation**: Created when first request is made without conversation_id, continues with subsequent requests
- **Request/Response Cycle**: New request triggers AI processing which may result in tool calls and a final response
- **Tool Execution**: Each tool call results in a database operation and a result returned to the AI agent