# Quickstart Guide: Remove explicit User ID prompting and add automatic multi-language response matching

## Overview
This guide explains how to implement the seamless user ID handling and automatic language response matching for the AI Todo Chatbot.

## Prerequisites
- Completed Phase I & II implementation (existing chatbot functionality)
- Access to Cohere API or compatible API for language model
- JWT authentication system in place
- Existing MCP tools for task management

## Setup Steps

### 1. Update Chat Endpoint
Modify the chat API endpoint to inject authenticated user context:

```python
# In backend/src/api/chat_routes.py
@router.post("/chat", response_model=ChatResponse)
def chat(
    request: Request,
    chat_request: ChatRequest,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    # Process the chat request using the authenticated user's ID
    result = ChatService.process_chat_message(
        session=session,
        user_id=int(current_user_id),  # Use the ID from JWT token
        conversation_id=chat_request.conversation_id,
        message=chat_request.message
    )
    return ChatResponse(
        conversation_id=result["conversation_id"],
        response=result["response"],
        tool_calls=result.get("tool_calls", [])
    )
```

### 2. Create Tool Wrapper
Create a wrapper for MCP tools to automatically inject user_id:

```python
# Example wrapper for tools
def create_authenticated_tool(tool_func, user_id_from_context):
    def wrapped_tool(*args, **kwargs):
        # Automatically inject user_id from context
        kwargs['user_id'] = user_id_from_context
        return tool_func(*args, **kwargs)
    return wrapped_tool
```

### 3. Update System Prompt
Enhance the agent's system prompt with language and user handling instructions:

```
You are a helpful todo assistant.
You already know who the user is — never ask for their user ID or name.
Always respond in the exact same language the user is currently writing in,
even if they switch languages mid-conversation.
```

### 4. Test the Implementation
Verify the new functionality works:

```bash
# Test creating a task without specifying user ID
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{"message": "Add a task to buy groceries"}'

# Test in different languages
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{"message": "کام شامل کریں"}'  # Urdu
```

## Expected Behavior
- The chatbot should never ask for user ID when performing task operations
- The chatbot should respond in the same language as the user's input
- All task operations should be associated with the authenticated user
- User data isolation should be maintained

## Troubleshooting
- If user ID prompts still appear, verify that the JWT token is being properly decoded
- If language detection isn't working, check that the system prompt is properly updated
- If tasks are not associated with the correct user, verify that user_id is being injected into tool calls