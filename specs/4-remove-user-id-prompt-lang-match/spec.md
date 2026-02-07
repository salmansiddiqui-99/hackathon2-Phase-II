# Feature Specification: Remove explicit User ID prompting and add automatic multi-language response matching

**Feature Branch**: `4-remove-user-id-prompt-lang-match`
**Created**: 2026-02-05
**Status**: Draft
**Input**: User description: "Phase III Extension: Remove explicit User ID prompting + Add automatic multi-language response matching user's input language

Target audience: Hackathon participants and judges evaluating natural, frictionless chatbot UX and intelligent language handling

Focus: Improve the conversational experience of the Phase III AI Todo Chatbot so that:

1. The chatbot NEVER asks the user for their User ID when performing CRUD operations (add, update, complete, delete, list tasks)
2. The chatbot automatically detects the language used in the user's message and responds in the same language (multi-language support without explicit selection)

Success criteria:
- **User ID handling**:
  - The chatbot infers the authenticated user automatically from the JWT token sent with every /api/{user_id}/chat request
  - In all tool calls (add_task, list_tasks, complete_task, delete_task, update_task), the user_id parameter is filled from the authenticated context — never from user input
  - If the user tries to mention or provide a user ID in natural language, the agent ignores it and uses the authenticated one
  - No message ever contains phrases like "What is your user ID?", "Please provide your ID", "Whose tasks?", etc.
- **Language matching**:
  - Chatbot detects the primary language of the user's input message
  - All responses (normal text + confirmations + error messages) are generated in the same detected language
  - Supported languages at minimum: English + Urdu (as per bonus feature) + any major language the chosen LLM (Cohere Command family) handles well
  - System prompt updated to enforce: "Always respond in the exact same language the user is currently using"
  - Language detection is implicit (done by the LLM itself) — no external library required
- All Basic Level todo operations remain fully functional via natural language
- No regression in existing behavior (context preservation, tool calling accuracy, confirmation style)

Constraints:
- Must stay within current architecture: ChatKit → FastAPI /chat → OpenAI Agents SDK agent → Cohere Compatibility API → MCP tools
- User authentication & JWT still required (no anonymous mode)
- Do NOT add new database fields or change MCP tool signatures
- Language support implemented purely via system prompt engineering and LLM capabilities — no translation API
- Keep using Cohere Trial / Compatibility API layer (no model or provider change)
- All changes must be spec-driven and generated via Claude Code / subagents

Not building:
- Explicit language selection menu or command
- Asking user to choose language
- Storing preferred language per user in database
- Adding new endpoints or changing /chat signature
- Implementing client-side language detection
- Supporting right-to-left layout adjustments in ChatKit (UI remains LTR unless bonus CSS added)

Bonus alignment:
- Directly contributes to "Multi-language Support – Support Urdu in chatbot" (+100 points)
- Improves overall UX → higher chance of strong demo video impression

This extension makes the chatbot significantly more natural, user-friendly, and production-like while staying fully compliant with the hackathon Phase III requirements and architecture."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Seamless task operations without user ID prompts (Priority: P1)

As a user, I want to interact with the AI chatbot naturally without being interrupted to provide my User ID, so that I can focus on managing my tasks seamlessly. When I say "Add a task to buy groceries", the chatbot should automatically associate this with my authenticated account without asking "What is your user ID?".

**Why this priority**: This is fundamental to the user experience improvement and directly addresses the core problem of friction in the chatbot interaction.

**Independent Test**: Can be fully tested by authenticating with JWT and performing task operations (create, update, complete, delete) without the chatbot requesting User ID, delivering improved conversational flow.

**Acceptance Scenarios**:

1. **Given** user is authenticated with JWT token, **When** user requests a task operation like "Add a task to buy groceries", **Then** the task is created for the authenticated user without requesting user ID
2. **Given** user is authenticated with JWT token, **When** user requests multiple task operations in sequence, **Then** all operations are performed on the authenticated user's data without prompting for user ID

---

### User Story 2 - Automatic language detection and response (Priority: P1)

As a user speaking in my native language, I want the AI chatbot to detect and respond in the same language, so that I can communicate naturally without switching to English or specifying my language preference. When I say "کام شامل کریں" (Urdu for "Add task"), the chatbot should respond in Urdu.

**Why this priority**: This directly enables multi-language support as specified in the bonus feature and improves accessibility for non-English speakers.

**Independent Test**: Can be fully tested by sending messages in different languages and verifying the chatbot responds in the same language, delivering improved inclusivity.

**Acceptance Scenarios**:

1. **Given** user sends a message in a specific language (e.g., Urdu), **When** the chatbot processes the request, **Then** the response is delivered in the same language
2. **Given** user sends messages in various supported languages, **When** conversation continues, **Then** the chatbot maintains language consistency throughout the session

---

### User Story 3 - Maintained security and user isolation (Priority: P2)

As a system administrator, I want to ensure that removing explicit user ID prompts doesn't compromise user data isolation, so that users can only access their own tasks even without explicitly providing their user ID. The system should continue to securely authenticate users through JWT tokens.

**Why this priority**: Critical for maintaining security standards and preventing unauthorized access to other users' data.

**Independent Test**: Can be tested by verifying that all task operations still validate against the authenticated user's JWT token, delivering secure data access.

**Acceptance Scenarios**:

1. **Given** user is authenticated with JWT token, **When** user performs task operations, **Then** only that user's tasks are accessed regardless of what they mention in natural language
2. **Given** user attempts to reference another user's ID in natural language, **When** processing occurs, **Then** the system ignores the reference and operates on the authenticated user's data

---

### Edge Cases

- What happens when a user tries to mention or provide a user ID in natural language?
- How does system handle a user switching between languages mid-conversation?
- What occurs when the language detection fails to identify the input language?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST automatically infer the authenticated user from the JWT token for all chat and task operations
- **FR-002**: System MUST NOT prompt users for their User ID during any task operations (create, update, complete, delete, list)
- **FR-003**: System MUST populate the user_id parameter in all MCP tool calls from the authenticated context, never from user input
- **FR-004**: System MUST ignore any user ID references provided in natural language and use the authenticated user's ID
- **FR-005**: System MUST detect the primary language of the user's input message automatically
- **FR-006**: System MUST respond in the same language as the user's input message
- **FR-007**: System MUST support English and Urdu languages at minimum, with capability to handle other major languages
- **FR-008**: System MUST maintain all existing task management functionality via natural language
- **FR-009**: System MUST preserve existing behavior for context preservation and tool calling accuracy
- **FR-010**: System MUST ensure user isolation remains intact despite removal of explicit user ID prompts

### Key Entities

- **Authenticated User**: Represents the logged-in user identified through JWT token, with exclusive access to their own task data
- **Task**: Represents a user-defined task with properties like title, description, completion status, and association to the authenticated user

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Zero prompts for user ID during task operations (create, update, complete, delete, list) after authentication
- **SC-002**: 100% of chatbot responses match the language of the corresponding user input
- **SC-003**: At least English and Urdu languages supported with 95% accuracy in both detection and response
- **SC-004**: All existing task operations remain functional with 99% success rate after removing user ID prompts
- **SC-005**: User satisfaction increases by 30% as measured by reduced friction in chatbot interactions
- **SC-006**: User data isolation remains 100% secure with no cross-user data access