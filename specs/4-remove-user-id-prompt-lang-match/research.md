# Research: Remove explicit User ID prompting and add automatic multi-language response matching

## Overview
This research document outlines the implementation approach for removing explicit User ID prompting and adding automatic multi-language response matching in the AI Todo Chatbot.

## Technical Decision: Context Injection
**Decision**: Inject authenticated user_id from FastAPI request into agent run context
**Rationale**: This approach eliminates the need to pass user_id through natural language, keeping the interaction seamless while maintaining security.
**Implementation**: Modify the chat endpoint to pass the decoded user_id from JWT into the agent context.

## Technical Decision: Tool Wrapper Layer
**Decision**: Wrap all MCP tools with automatic user_id injection from context
**Rationale**: This keeps the existing tool signatures unchanged while allowing automatic population of user_id.
**Implementation**: Create decorators or wrapper functions that intercept tool calls and inject the user_id from the authenticated context.

## Technical Decision: System Prompt Enhancement
**Decision**: Update agent instructions to never ask for user ID and always respond in the same language as the user
**Rationale**: Pure LLM capability approach works well with Cohere Command models and requires no additional libraries.
**Implementation**: Enhance the system prompt with specific instructions about user identification and language matching.

## Implementation Steps

### 1. Authentication Context Injection
- Modify `chat_routes.py` to pass the decoded JWT user_id into the agent run context
- Ensure the user_id is accessible to the AI agent during processing

### 2. MCP Tool Wrapping
- Create a wrapper mechanism for all MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
- The wrapper should automatically inject the authenticated user_id into tool parameters
- Maintain original tool signatures for compatibility

### 3. System Prompt Updates
- Enhance the agent's system prompt with instructions to:
  - Never ask for user ID or name
  - Always respond in the exact same language the user is currently writing in
  - Automatically detect language from user input

### 4. Language Handling Approach
- Leverage LLM's inherent language detection and response capabilities
- No external language detection libraries needed
- System prompt enforcement will ensure consistent behavior

## Architecture Impact
- Minimal changes to existing architecture
- Maintains security through JWT-based user identification
- Preserves existing functionality while adding seamless UX
- Backwards compatible with current API structure

## Risk Assessment
- Low risk as changes are primarily additive and don't modify core functionality
- User isolation maintained through JWT authentication
- Language handling relies on proven LLM capabilities