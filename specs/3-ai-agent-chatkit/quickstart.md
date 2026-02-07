# Quickstart Guide: AI Agent & ChatKit Integration

## Overview
This guide outlines the implementation of the AI Agent & ChatKit Integration feature, including OpenRouter configuration, AI agent initialization with MCP tools, prompt engineering, and ChatKit frontend setup.

## Prerequisites
- Backend running with existing MCP tools from Part 2
- OpenRouter API access with provided credentials
- Next.js environment for ChatKit frontend
- JWT authentication system from Phase II

## Implementation Steps

### 1. OpenRouter Configuration
Set up OpenRouter client in `backend/src/ai/openrouter_config.py`:

1. Configure base_url to https://openrouter.ai/api/v1
2. Set API key to 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
3. Specify model as tngtech/deepseek-r1t2-chimera:free
4. Create OpenRouter client with proper error handling

### 2. AI Agent Initialization
Create the AI agent in `backend/src/ai/agent.py`:

1. Initialize OpenAI Agents SDK client
2. Register MCP tools as available functions
3. Configure agent with system prompt
4. Set up tool calling mechanism with function definitions

### 3. Prompt Engineering
Create system prompt in `backend/src/ai/prompt.py`:

1. Define exact agent behavior rules for task operations
2. Specify natural language command interpretations
3. Include error handling and fallback responses
4. Define conversation context management

### 4. Chat Orchestration
Enhance the existing chat endpoint in `backend/src/api/chat_routes.py`:

1. Route requests to AI agent instead of simple processing
2. Process agent responses and tool calls
3. Ensure proper user_id validation and isolation
4. Maintain stateless operation with database persistence

### 5. ChatKit Frontend Configuration
Set up ChatKit UI in `frontend/src/`:

1. Install OpenAI ChatKit dependencies
2. Configure ChatKit to connect to POST /api/{user_id}/chat
3. Handle JWT authentication tokens
4. Configure domain allowlist for production

### 6. Authentication Bridge
Ensure JWT token flow in `frontend/src/lib/auth.ts`:

1. Pass JWT tokens from ChatKit to backend calls
2. Validate token authenticity and user_id matching
3. Handle token expiration and refresh
4. Secure token storage and transmission

## Configuration
- Ensure OpenRouter API credentials are properly secured
- Verify JWT authentication tokens are passed correctly between frontend and backend
- Confirm MCP tools are properly registered with the AI agent
- Test domain allowlist configuration for production deployment

## Testing
1. Test natural language command: "Add task buy milk" → verify task created
2. Test natural language command: "List my tasks" → verify tasks returned
3. Test natural language command: "Mark task 1 as done" → verify status updated
4. Test natural language command: "Delete task 3" → verify removal
5. Test natural language command: "Update task 2 title to groceries" → verify change
6. Test error handling with invalid commands → verify helpful error messages
7. Test multi-turn conversations → verify context preservation
8. Test user isolation → verify users can't access other users' tasks