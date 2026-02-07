---
description: "Task list for switching LLM provider from OpenRouter to Cohere (Free Trial Tier)"
---

# Tasks: Switch LLM Provider from OpenRouter to Cohere (Free Trial Tier)

**Input**: Design documents from `/specs/[###-feature-name]/`
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

- [X] T001 Create/update .env file with COHERE_API_KEY=SqnhRaifcIHJyGeTqODA955lm5VvIlP1cJHYtDmM
- [X] T002 Update .env.example with COHERE_API_KEY placeholder
- [ ] T003 [P] Verify Cohere API key and endpoint accessibility

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Create Cohere configuration module in backend/src/ai/cohere_config.py
- [X] T005 [P] Update backend/src/ai/openrouter_config.py to deprecate/remove OpenRouter references
- [X] T006 Configure AsyncOpenAI client with Cohere settings in backend/src/ai/cohere_config.py
- [X] T007 Set up Cohere base URL to https://api.cohere.ai/compatibility/v1 in cohere_config.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---
## Phase 3: User Story 1 - Maintain Chat Functionality with New LLM Provider (Priority: P1) 🎯 MVP

**Goal**: Ensure the chatbot continues working seamlessly after switching to Cohere LLM provider

**Independent Test**: Verifying that all existing chatbot interactions (adding tasks, listing tasks, completing tasks, etc.) continue to work identically after the provider switch.

### Implementation for User Story 1

- [X] T008 [P] [US1] Update model selection in agent configuration to command-r7b-12-2024 in backend/src/ai/agent.py
- [X] T009 [US1] Update RunConfig in backend/src/ai/agent.py to use Cohere-compatible model and client
- [X] T010 [US1] Modify AIAgent initialization to use Cohere client configuration
- [X] T011 [US1] Test chat functionality with Cohere endpoint by sending "Add task buy milk tomorrow"
- [X] T012 [US1] Verify task creation works via MCP tool with Cohere integration
- [X] T013 [US1] Test "List my tasks" functionality to ensure tasks are returned correctly
- [X] T014 [US1] Test "Complete task" functionality to verify task status updates

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---
## Phase 4: User Story 2 - Preserve All AI Agent Behaviors and Tools (Priority: P1)

**Goal**: Ensure the AI agent continues using all existing MCP tools with identical behavior after the provider switch

**Independent Test**: Verifying that all MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) continue to work identically after the provider switch.

### Implementation for User Story 2

- [X] T015 [P] [US2] Verify all existing MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) remain unchanged
- [X] T016 [US2] Test tool-calling functionality with Cohere model to ensure compatibility
- [X] T017 [US2] Verify tool schemas remain compatible with Cohere's implementation
- [X] T018 [US2] Test update_task functionality specifically to ensure proper invocation
- [X] T019 [US2] Validate multi-tool sequences work properly with Cohere responses
- [X] T020 [US2] Confirm agent behavior rules remain identical to OpenRouter implementation

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---
## Phase 5: User Story 3 - Configure New LLM Provider with Trial Account (Priority: P2)

**Goal**: Configure the AI agent to use Cohere's compatibility API with the provided trial key for cost-effective development

**Independent Test**: Verifying that LLM requests are successfully routed through Cohere's API endpoint with the provided API key and model.

### Implementation for User Story 3

- [X] T021 [P] [US3] Configure AI agent to use Cohere's compatibility API with provided trial key in backend/src/ai/agent.py
- [X] T022 [US3] Verify LLM inference calls route through Cohere's Compatibility API endpoint
- [X] T023 [US3] Test inference request processing through Cohere's API successfully
- [X] T024 [US3] Validate usage respects Cohere's trial limits (~20 req/min, ~1000 calls/month)
- [X] T025 [US3] Implement basic rate limit handling if needed for trial compliance

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all be independently functional

---
## Phase 6: User Story 4 - Maintain User Isolation and Security (Priority: P1)

**Goal**: Ensure user data remains isolated from other users after the provider switch to maintain security

**Independent Test**: Verifying that users can only access their own conversations and tasks after the provider switch.

### Implementation for User Story 4

- [X] T026 [P] [US4] Test that user isolation mechanisms continue to function properly with Cohere integration
- [X] T027 [US4] Verify users only see their own conversations after Cohere integration
- [X] T028 [US4] Confirm access controls reject attempts to access other users' data
- [X] T029 [US4] Test security mechanisms remain intact during Cohere API interactions
- [X] T030 [US4] Validate no data leakage occurs through Cohere's LLM provider

**Checkpoint**: All user stories should now be independently functional

---
## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T031 [P] Update documentation in README.md about Cohere Trial usage and limitations
- [X] T032 Update CLAUDE.md with implementation notes about Cohere Trial integration
- [X] T033 Document trial usage constraints (1000 calls/month, 20 chat/min) in docs/
- [X] T034 Add usage guidelines for demo purposes in documentation
- [X] T035 Test full end-to-end chat experience with Cohere integration
- [X] T036 Validate all Phase III functionality preserved after Cohere switch
- [X] T037 Run user isolation tests to confirm security measures remain intact
- [X] T038 Update any remaining OpenRouter references to Cohere terminology

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
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P1)**: Can start after Foundational (Phase 2) - May integrate with other stories but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---
## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Update model selection in agent configuration to command-r7b-12-2024 in backend/src/ai/agent.py"
Task: "Update RunConfig in backend/src/ai/agent.py to use Cohere-compatible model and client"
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
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
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