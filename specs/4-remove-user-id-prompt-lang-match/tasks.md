---
description: "Task list for implementing Phase III Extension to remove explicit User ID prompting and add automatic multi-language response matching"
---

# Tasks: Remove explicit User ID prompting and add automatic multi-language response matching

**Input**: Design documents from `/specs/4-remove-user-id-prompt-lang-match/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 [P] Update chat API endpoint to remove user_id from path in backend/src/api/chat_routes.py
- [X] T002 [P] Update task API endpoints to remove user_id from path in backend/src/api/task_routes.py
- [X] T003 [P] Update frontend API calls to remove user_id from path in frontend/src/lib/api.ts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 [P] Create tool wrapper function to inject user_id from context in backend/src/mcp/tools.py
- [X] T005 [P] Update chat service to pass user_id from JWT to agent in backend/src/services/chat_service.py
- [X] T006 [P] Update chat endpoint to use JWT user_id directly in backend/src/api/chat_routes.py
- [X] T007 [P] Update task endpoints to use JWT user_id directly in backend/src/api/task_routes.py
- [X] T008 [P] Update frontend API client to remove user_id parameters in frontend/src/lib/api.ts

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Seamless task operations without user ID prompts (Priority: P1) 🎯 MVP

**Goal**: Users can interact with the AI chatbot naturally without being interrupted to provide their User ID during task operations

**Independent Test**: Can be fully tested by authenticating with JWT and performing task operations (create, update, complete, delete) without the chatbot requesting User ID, delivering improved conversational flow.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests first, ensure they fail before implementation**

- [ ] T009 [P] [US1] Contract test for updated chat API endpoint in backend/tests/contract/test_chat_api.py
- [ ] T010 [P] [US1] Integration test for task operations without user ID prompts in backend/tests/integration/test_task_operations.py

### Implementation for User Story 1

- [X] T011 [P] [US1] Update system prompt to prevent user ID requests in backend/src/ai/agent.py
- [X] T012 [US1] Modify chat service to ensure user_id is always from JWT in backend/src/services/chat_service.py
- [X] T013 [US1] Test that chatbot does not prompt for user ID during task operations
- [X] T014 [US1] Update frontend components to use new API endpoints in frontend/src/components/AIChat.tsx
- [X] T015 [US1] Update ChatKit to use new API endpoints in frontend/src/components/ChatKit/ChatKit.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Automatic language detection and response (Priority: P1)

**Goal**: The AI chatbot automatically detects the language used in the user's message and responds in the same language

**Independent Test**: Can be fully tested by sending messages in different languages and verifying the chatbot responds in the same language, delivering improved inclusivity.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T016 [P] [US2] Contract test for language detection in backend/src/ai/agent.py
- [ ] T017 [P] [US2] Integration test for multi-language responses in backend/tests/integration/test_language_support.py

### Implementation for User Story 2

- [X] T018 [P] [US2] Update agent system prompt for language detection in backend/src/ai/agent.py
- [X] T019 [US2] Test that chatbot responds in the same language as user input (English, Urdu)
- [X] T020 [US2] Validate language consistency during mid-conversation switches
- [X] T021 [US2] Test language detection with mixed language inputs
- [X] T022 [US2] Verify responses in various supported languages

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Maintained security and user isolation (Priority: P2)

**Goal**: Ensure that removing explicit user ID prompts doesn't compromise user data isolation - users can only access their own tasks

**Independent Test**: Can be tested by verifying that all task operations still validate against the authenticated user's JWT token, delivering secure data access.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T023 [P] [US3] Contract test for user data isolation in backend/tests/contract/test_security.py
- [ ] T024 [P] [US3] Integration test for user ID ignoring in backend/tests/integration/test_user_isolation.py

### Implementation for User Story 3

- [X] T025 [P] [US3] Update MCP tools to enforce user_id from JWT context in backend/src/mcp/tools.py
- [X] T026 [US3] Test that user cannot access other users' tasks despite natural language mentions
- [X] T027 [US3] Verify natural language user ID references are ignored in favor of JWT
- [X] T28 [US3] Validate that all database queries are filtered by authenticated user
- [X] T029 [US3] Test edge case where user tries to mention another user's ID in natural language

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T030 [P] Update documentation in specs/4-remove-user-id-prompt-lang-match/
- [X] T031 Code cleanup and refactoring of redundant user ID handling
- [X] T032 Performance optimization for language detection
- [X] T033 [P] Additional unit tests in backend/tests/unit/
- [X] T034 Security hardening for language input validation
- [X] T035 Run quickstart.md validation to confirm all features work

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for updated chat API endpoint in backend/tests/contract/test_chat_api.py"
Task: "Integration test for task operations without user ID prompts in backend/tests/integration/test_task_operations.py"

# Launch all implementation tasks for User Story 1 together:
Task: "Update system prompt to prevent user ID requests in backend/src/ai/agent.py"
Task: "Update frontend components to use new API endpoints in frontend/src/components/AIChat.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence