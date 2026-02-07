# Feature Specification: Natural Task Reference by Title

**Feature Branch**: `5-natural-task-reference-by-title`
**Created**: 2026-02-05
**Status**: Draft
**Input**: User description: "Phase III Extension: Natural Task Reference by Title (No Task ID Prompting)

Target audience: Hackathon participants and judges evaluating natural, frictionless, human-like chatbot conversation design

Focus: Make the Phase III AI Todo Chatbot handle update, complete, delete, and (if ambiguous) list operations using **task title** instead of requiring the user to know or provide numeric Task IDs.

The goal is to eliminate all prompts asking for Task ID — similar to how we already removed User ID prompting.

Success criteria:
- The chatbot **never** asks the user for a numeric Task ID in any scenario
- Supported natural language patterns that should work without ID:
  - "complete my task buy groceries"
  - "mark 'call mom' as done"
  - "delete the task named finish report"
  - "update 'morning run' to 'morning yoga at 7am'"
  - "reschedule my dentist appointment to next Tuesday"
- When title is ambiguous (multiple tasks with very similar/identical titles):
  - Chatbot asks for **clarification by showing short list of matching titles** (not IDs)
  - Example response:
    "I found two tasks with similar titles:
    1. buy groceries
    2. buy groceries for party
    Which one do you mean?"
  - User can reply with number (1/2), full title, or more detail → chatbot proceeds
- When title is unique → action is performed silently and confirmed
- List operation ("show my tasks", "list todos") still shows tasks with titles + status + other visible fields — no IDs shown to user unless absolutely necessary for disambiguation
- Add / update still work by title (creation doesn't need ID anyway)
- All previous improvements remain:
  - No User ID ever asked
  - Responses in the same language the user is using
- Maintains 100% correctness: wrong title → helpful message ("I couldn't find a task called 'xyz'. Here are your current tasks: …")

Constraints:
- Do **not** change the MCP tool signatures (they still expect task_id internally)
- The intelligence to map title → task_id must happen **inside the agent / before tool call**
  - Agent queries list_tasks first (internally) when title-based command is detected
  - Matches title (case-insensitive, partial match with tolerance)
  - If exactly one match → use its id for complete/delete/update
  - If multiple → ask user for clarification (text response, no tool call yet)
  - If none → inform user and optionally list recent/open tasks
- Implementation must stay within current stack:
  - OpenAI Agents SDK + Cohere Compatibility API
  - Existing 5 MCP tools
  - Stateless /chat endpoint
  - No new database queries outside existing tools
- All logic implemented via **stronger system prompt + possible few-shot examples**
  - Preferred: pure prompt engineering (zero code change to tools or endpoint)
  - Allowed: small wrapper/helper function inside agent if prompt alone is not reliable enough
- Keep demo-friendly: short, clear clarification messages

Not building:
- Showing internal Task IDs to the user in normal flow
- Forcing user to use numbers/IDs
- Adding new MCP tools (e.g. get_task_by_title)
- Changing database schema
- Client-side title search (everything server/agent side)
- Strict exact-match-only (fuzzy/partial matching should be supported via LLM reasoning)

Bonus alignment:
- Makes chatbot significantly more user-friendly and natural
- Directly improves UX score in judging (especially in demo video)
- Builds on previous "no user ID" and "multi-language" improvements

This change removes the last major point of friction in title-based task management — users should be able to speak to the bot like they would speak to a human assistant."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Natural task operations using titles (Priority: P1)

As a user, I want to interact with the AI chatbot using natural language that refers to tasks by their titles, so that I can manage my tasks without having to remember or provide numeric Task IDs. When I say "complete my task buy groceries", the chatbot should automatically identify and operate on the task with that title without asking for a numeric ID.

**Why this priority**: This is fundamental to the user experience improvement and directly addresses the core problem of friction in the chatbot interaction when managing tasks.

**Independent Test**: Can be fully tested by authenticating with JWT and performing task operations (complete, delete, update) using titles without the chatbot requesting numeric Task IDs, delivering improved conversational flow.

**Acceptance Scenarios**:

1. **Given** user has a task titled "buy groceries", **When** user requests "complete my task buy groceries", **Then** the task is completed without requesting numeric Task ID
2. **Given** user has a task titled "call mom", **When** user requests "mark 'call mom' as done", **Then** the task is marked as complete without requesting numeric Task ID
3. **Given** user has a task titled "finish report", **When** user requests "delete the task named finish report", **Then** the task is deleted without requesting numeric Task ID

---

### User Story 2 - Handle ambiguous titles with clarification (Priority: P1)

As a user, I want the chatbot to handle cases where I have multiple tasks with similar titles by asking for clarification in a natural way, so that I can easily specify which task I'm referring to without having to remember numeric IDs. When I have two tasks with similar titles and I request an action, the chatbot should show the titles and let me clarify.

**Why this priority**: Critical for handling real-world scenarios where users may have multiple tasks with similar titles, maintaining the natural interaction without falling back to numeric IDs.

**Independent Test**: Can be fully tested by creating multiple tasks with similar titles and requesting an action on a generic reference, verifying that the chatbot asks for clarification by showing the titles (not IDs) and correctly processes the follow-up response.

**Acceptance Scenarios**:

1. **Given** user has tasks titled "buy groceries" and "buy groceries for party", **When** user requests "complete buy groceries", **Then** the chatbot shows both titles and asks for clarification
2. **Given** chatbot has asked for clarification between similar titles, **When** user responds with the number of the desired task, **Then** the correct task is operated on
3. **Given** chatbot has asked for clarification between similar titles, **When** user responds with the full title of the desired task, **Then** the correct task is operated on

---

### User Story 3 - Natural updates and rescheduling by title (Priority: P2)

As a user, I want to update and reschedule tasks using natural language that refers to them by title, so that I can modify tasks without remembering numeric IDs. When I say "update 'morning run' to 'morning yoga at 7am'" or "reschedule my dentist appointment to next Tuesday", the chatbot should handle these requests naturally.

**Why this priority**: Enhances the core functionality by allowing natural updates and rescheduling, building on the basic task operations to provide a more complete natural interaction experience.

**Independent Test**: Can be tested by performing update and reschedule operations using title references, ensuring the chatbot correctly identifies the task and modifies it without asking for numeric IDs.

**Acceptance Scenarios**:

1. **Given** user has a task titled "morning run", **When** user requests "update 'morning run' to 'morning yoga at 7am'", **Then** the task title is updated appropriately
2. **Given** user has a task titled "dentist appointment", **When** user requests "reschedule my dentist appointment to next Tuesday", **Then** the task is updated with new details

---

### Edge Cases

- What happens when a user refers to a task that doesn't exist?
- How does system handle tasks with identical titles?
- What occurs when partial title matches return multiple possibilities?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow task operations (complete, delete, update) using title references instead of numeric IDs
- **FR-002**: System MUST NOT prompt users for numeric Task IDs during any task operations (complete, delete, update)
- **FR-003**: System MUST map title references to internal task_ids within the agent before MCP tool calls
- **FR-004**: System MUST handle fuzzy/partial title matching to find tasks using LLM reasoning
- **FR-005**: System MUST ask for clarification when title references match multiple tasks
- **FR-006**: System MUST show task titles (not IDs) during clarification prompts
- **FR-007**: System MUST accept clarification responses by number selection or full title
- **FR-008**: System MUST maintain existing functionality for all previous improvements (no user ID prompts, language matching)
- **FR-009**: System MUST provide helpful error messages when task titles are not found
- **FR-010**: System MUST continue to show task lists with titles and status without exposing numeric IDs

### Key Entities

- **Task**: Represents a user-defined task with properties like title, description, completion status, and association to the authenticated user
- **User Intent**: Represents the user's natural language request that needs to be mapped to specific task operations

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Zero prompts for numeric Task IDs during task operations (complete, delete, update) after implementation
- **SC-002**: 100% of supported natural language patterns work without requiring Task IDs
- **SC-003**: At least 95% accuracy in mapping title references to correct internal task_ids
- **SC-004**: All existing task operations remain functional with 99% success rate after removing numeric ID dependencies
- **SC-005**: User satisfaction increases by 30% as measured by reduced friction in task management interactions
- **SC-006**: Ambiguous title scenarios handled correctly with appropriate clarification 100% of the time