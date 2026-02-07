# Research: Natural Task Reference by Title

## Overview
This research document outlines the implementation approach for enabling natural task reference by title, eliminating the need for numeric Task ID prompts in the AI Todo Chatbot.

## Technical Decision: System Prompt Major Upgrade
**Decision**: Completely rewrite agent instructions to forbid asking for task IDs and guide title-based operations
**Rationale**: This approach ensures the agent never falls back to requesting numeric IDs, maintaining the natural interaction flow.
**Implementation**: Redesign the system prompt with clear instructions against numeric ID requests and guidelines for title-based operations.

## Technical Decision: Title-Based Reasoning Guidelines
**Decision**: Add detailed few-shot examples and rules for title → task_id resolution within the system prompt
**Rationale**: By providing clear examples and reasoning patterns, the LLM can better understand how to match user-provided titles to internal task IDs.
**Implementation**: Include example scenarios with step-by-step resolution processes in the system prompt.

## Technical Decision: Internal Task Resolution Logic
**Decision**: Implement a process where the agent internally calls list_tasks when title-based commands are detected
**Rationale**: Allows the agent to match user-provided titles against the current task list without requiring users to provide numeric IDs.
**Implementation**:
- When title-based command detected, agent calls list_tasks internally
- Agent matches user title against returned task titles (fuzzy/partial/case-insensitive)
- If unique match → proceed with tool call using found task_id
- If multiple matches → respond with numbered list of matching titles (no IDs shown) and ask for clarification
- If no match → respond helpfully + optionally list recent/open tasks

## Technical Decision: Clarification Response Format
**Decision**: Design clean, natural disambiguation message template that shows titles without exposing internal IDs
**Rationale**: Maintains the human-like interaction by avoiding technical details while providing clear options for user clarification.
**Implementation**: Create standardized templates for different clarification scenarios.

## Implementation Steps

### 1. System Prompt Rewrite
- Remove any language that allows for task ID requests
- Add explicit instruction: "NEVER ask for or mention numeric task IDs — users don't know them"
- Add instruction: "Always use task titles to identify which task the user means"

### 2. Title Resolution Rules
- Implement internal logic: When user says "complete X", "delete Y", "update Z":
  1. Call list_tasks to get current tasks
  2. Find best title match using fuzzy logic
  3. If unique → use its id for the action tool
  4. If multiple → ask user to choose by title or number (show titles only)
  5. If none → tell user and suggest alternatives

### 3. Clarification Templates
- Develop natural language templates for ambiguous title scenarios
- Ensure all responses refer to tasks by their titles, never by ID

### 4. Confirmation Messages Update
- Ensure all success/error confirmations use titles instead of IDs
- Maintain consistency in how tasks are referenced throughout the conversation

## Architecture Impact
- No changes to MCP tool signatures required (they still accept task_id internally)
- No database changes needed
- Agent-side logic handles title-to-ID mapping
- Maintains backward compatibility with existing functionality
- Preserves previous improvements (no user ID prompts, language matching)

## Risk Assessment
- Low risk as changes are primarily in the agent's system prompt and reasoning logic
- No changes to underlying data structures or API contracts
- Title matching logic is contained within the agent, minimizing impact on other components
- Fallback behavior is well-defined for edge cases