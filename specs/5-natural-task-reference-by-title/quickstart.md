# Quickstart Guide: Natural Task Reference by Title

## Overview
This guide explains how to implement natural task reference by title, allowing users to interact with the AI Todo Chatbot using natural language that refers to tasks by their titles instead of numeric IDs.

## Prerequisites
- Completed Phase I, II, and previous Phase III implementations (no user ID prompting, multi-language support)
- Access to Cohere API or compatible API for language model
- Existing MCP tools for task management
- Working chatbot with stateless architecture

## Setup Steps

### 1. Update System Prompt
Enhance the agent's system prompt with title-based operation instructions:

```
You are a helpful todo assistant.
- NEVER ask for or mention numeric task IDs — users don't know them.
- Always use task titles to identify which task the user means.
- When the user says "complete X", "delete Y", "update Z" — internally:
  1. Call list_tasks to get current tasks
  2. Find best title match using fuzzy/partial/case-insensitive matching
  3. If unique → use its id for the action tool
  4. If multiple → ask user to choose by title or number (show titles only)
  5. If none → tell user and suggest alternatives
- In all responses: refer to tasks by their titles, never by ID.
- You already know who the user is — never ask for their user ID or name.
- Always respond in the exact same language the user is currently writing in,
  even if they switch languages mid-conversation.
```

### 2. Add Few-Shot Examples
Include examples in the prompt to guide the agent:

```
Example interactions:
User: "complete my task buy groceries"
Internal: Calls list_tasks, finds task with title "buy groceries", completes it.

User: "delete finish report"
Internal: Calls list_tasks, finds task with title "finish report", deletes it.

User: "update morning run to evening walk"
Internal: Calls list_tasks, finds task with title "morning run", updates it to "evening walk".

User: "mark 'call mom' as done"
Internal: Calls list_tasks, finds task with title "call mom", marks as complete.
```

### 3. Implement Disambiguation Templates
Add templates for when multiple titles match:

```
If multiple tasks match the user's title reference, respond with:

"I found multiple tasks with similar titles:
1. {title1}
2. {title2}
...
Which one do you mean?"
```

### 4. Test the Implementation
Verify the new functionality works:

```bash
# Test completing a task by title
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{"message": "complete buy groceries"}'

# Test deleting a task by title
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{"message": "delete finish report"}'

# Test updating a task by title
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{"message": "update morning run to evening walk"}'

# Test ambiguous title scenario
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{"message": "complete buy milk"}'
```

## Expected Behavior
- The chatbot should never ask for numeric Task IDs when performing operations
- Title-based commands should work with fuzzy matching (partial matches, case-insensitive)
- When titles are ambiguous, the bot should show the matching titles and ask for clarification
- All responses should refer to tasks by their titles, not IDs
- Previous functionality (no user ID prompts, language matching) should remain intact

## Troubleshooting
- If numeric ID prompts still appear, verify that the system prompt has been updated with clear "NEVER ask for task IDs" instructions
- If title matching is too strict, check that fuzzy/partial matching is properly communicated in the system prompt
- If clarification messages still show IDs, verify that the disambiguation templates only reference titles