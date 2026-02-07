# Implementation Plan: Natural Task Reference by Title

**Branch**: `5-natural-task-reference-by-title` | **Date**: 2026-02-05 | **Spec**: [specs/5-natural-task-reference-by-title/spec.md]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement Phase III Extension to enable natural task reference by title, eliminating the need for users to provide numeric Task IDs during operations. This involves rewriting the agent system prompt to forbid asking for task IDs, adding title-based reasoning guidelines, implementing internal task resolution logic, and updating clarification response formats.

## Technical Context

**Language/Version**: Python 3.11, TypeScript/JavaScript, FastAPI
**Primary Dependencies**: FastAPI, OpenAI SDK, Cohere API compatibility layer, MCP tools
**Storage**: SQLModel/PostgreSQL for backend persistence
**Testing**: pytest for backend, Jest/React Testing Library for frontend
**Target Platform**: Web application with Next.js frontend and FastAPI backend
**Project Type**: Web
**Performance Goals**: Sub-second response times for chat interactions
**Constraints**: Must maintain existing functionality while adding title-based resolution, no changes to MCP tool signatures
**Scale/Scope**: Individual user task management with fuzzy title matching and clarification for ambiguous references

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The implementation adheres to the following constitutional principles:
- Maintain user data isolation through JWT-based authentication ✓
- Follow SDD methodology with minimal, testable changes ✓
- Preserve existing functionality while adding new features ✓
- Use consistent design patterns across the application ✓
- Ensure security is not compromised during feature enhancement ✓

All constitutional requirements have been verified as met with the implementation approach.

## Project Structure

### Documentation (this feature)

```text
specs/5-natural-task-reference-by-title/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── ai/
│   │   └── agent.py                 # AI agent system prompt and configuration
│   ├── api/
│   │   └── chat_routes.py          # Chat API endpoint
│   ├── mcp/
│   │   └── tools.py                # MCP tools (unchanged, still use task_id internally)
│   ├── middleware/
│   │   └── auth.py                 # JWT authentication middleware
│   └── services/
│       └── chat_service.py         # Chat service logic
└── tests/

frontend/
├── src/
│   ├── components/
│   │   ├── AIChat.tsx              # Chat UI component
│   │   └── ChatKit/
│   │       └── ChatKit.tsx         # Enhanced chat UI component
│   ├── lib/
│   │   └── api.ts                  # API client
│   └── types/
└── tests/
```

**Structure Decision**: Using the existing web application structure with separated frontend (Next.js) and backend (FastAPI) components to maintain consistency with the current architecture.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Agent-side title matching logic | Need to map titles to internal task_ids without changing MCP tool signatures | Changing MCP tools would break existing contracts |