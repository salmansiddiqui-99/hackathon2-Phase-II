---
description: "Task list for implementing Natural Task Reference by Title feature"
---

# Tasks: Natural Task Reference by Title

**Input**: Design documents from `/specs/5-natural-task-reference-by-title/`
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

- [X] T001 [P] Update system prompt to forbid asking for task IDs in backend/src/ai/agent.py
- [X] T002 [P] Add title-based reasoning guidelines to system prompt in backend/src/ai/agent.py
- [X] T003 [P] Add few-shot examples for title → task_id resolution in backend/src/ai/agent.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 [P] Implement internal task resolution logic in backend/src/ai/agent.py
- [X] T005 [P] Create clarification response templates in backend/src/ai/agent.py
- [X] T006 [P] Update confirmation messages to use titles in backend/src/ai/agent.py
- [X] T007 [P] Implement fuzzy/partial title matching logic in backend/src/ai/agent.py
- [X] T008 [P] Ensure all responses refer to tasks by titles, not IDs in backend/src/ai/agent.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural task operations using titles (Priority: P1) 🎯 MVP

**Goal**: Enable users to interact with the AI chatbot using natural language that refers to tasks by their titles without needing numeric Task IDs

**Independent Test**: Can be fully tested by authenticating with JWT and performing task operations (complete, delete, update) using titles without the chatbot requesting numeric Task IDs, delivering improved conversational flow.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests first, ensure they fail before implementation**

- [ ] T009 [P] [US1] Contract test for title-based task completion in backend/tests/contract/test_task_operations.py
- [ ] T010 [P] [US1] Integration test for "complete my task buy groceries" in backend/tests/integration/test_title_resolution.py

### Implementation for User Story 1

- [X] T011 [P] [US1] Implement internal list_tasks call when title-based command detected in backend/src/ai/agent.py
- [X] T012 [US1] Test title matching with exact match "buy groceries" in backend/tests/unit/test_title_matching.py
- [X] T013 [US1] Implement success confirmation using title instead of ID in backend/src/ai/agent.py
- [X] T014 [US1] Update frontend components to show title-based confirmations in frontend/src/components/AIChat.tsx
- [X] T015 [US1] Validate zero prompts for numeric Task IDs during title-based operations in backend/src/ai/agent.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Handle ambiguous titles with clarification (Priority: P1)

**Goal**: Handle cases where users have multiple tasks with similar titles by asking for clarification in a natural way without showing numeric IDs

**Independent Test**: Can be fully tested by creating multiple tasks with similar titles and requesting an action on a generic reference, verifying that the chatbot asks for clarification by showing the titles (not IDs) and correctly processes the follow-up response.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T016 [P] [US2] Contract test for clarification prompt when multiple titles match in backend/tests/contract/test_disambiguation.py
- [ ] T017 [P] [US2] Integration test for ambiguous title handling in backend/tests/integration/test_ambiguous_titles.py

### Implementation for User Story 2

- [X] T018 [P] [US2] Implement detection of multiple title matches in backend/src/ai/agent.py
- [X] T019 [US2] Create natural clarification response with title list (no IDs) in backend/src/ai/agent.py
- [X] T020 [US2] Implement handling of user's clarification response (number/title) in backend/src/ai/agent.py
- [X] T021 [US2] Test ambiguous title scenario with multiple similar titles in backend/tests/unit/test_disambiguation.py
- [X] T022 [US2] Validate that only titles (not IDs) are shown during clarification in backend/src/ai/agent.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Natural updates and rescheduling by title (Priority: P2)

**Goal**: Allow users to update and reschedule tasks using natural language that refers to them by title without remembering numeric IDs

**Independent Test**: Can be tested by performing update and reschedule operations using title references, ensuring the chatbot correctly identifies the task and modifies it without asking for numeric IDs.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T023 [P] [US3] Contract test for title-based task updates in backend/tests/contract/test_updates.py
- [ ] T024 [P] [US3] Integration test for reschedule operations by title in backend/tests/integration/test_reschedule.py

### Implementation for User Story 3

- [X] T025 [P] [US3] Implement title-based update operation logic in backend/src/ai/agent.py
- [X] T026 [US3] Implement reschedule operation handling by title in backend/src/ai/agent.py
- [X] T027 [US3] Test update command "update 'morning run' to 'morning yoga at 7am'" in backend/tests/unit/test_updates.py
- [X] T028 [US3] Test reschedule command "reschedule my dentist appointment to next Tuesday" in backend/tests/unit/test_reschedule.py
- [X] T029 [US3] Validate that updates maintain title-based references in backend/src/ai/agent.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T030 [P] Update documentation in specs/5-natural-task-reference-by-title/
- [X] T031 Code cleanup and refactoring of redundant ID-based logic
- [X] T032 Performance optimization for title matching algorithms
- [X] T033 [P] Additional unit tests in backend/tests/unit/
- [X] T034 Security hardening for title input validation
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
Task: "Contract test for title-based task completion in backend/tests/contract/test_task_operations.py"
Task: "Integration test for 'complete my task buy groceries' in backend/tests/integration/test_title_resolution.py"

# Launch all implementation tasks for User Story 1 together:
Task: "Implement internal list_tasks call when title-based command detected in backend/src/ai/agent.py"
Task: "Implement success confirmation using title instead of ID in backend/src/ai/agent.py"
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