# Implementation Plan: Remove explicit User ID prompting and add automatic multi-language response matching

**Branch**: `4-remove-user-id-prompt-lang-match` | **Date**: 2026-02-05 | **Spec**: [specs/4-remove-user-id-prompt-lang-match/spec.md]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement Phase III Extension to remove explicit User ID prompting and add automatic multi-language response matching for the AI Todo Chatbot. This involves enhancing the authentication context injection, wrapping MCP tools with automatic user_id injection, and updating system prompts to enforce language matching behavior.

## Technical Context

**Language/Version**: Python 3.11, TypeScript/JavaScript, FastAPI
**Primary Dependencies**: FastAPI, OpenAI SDK, Cohere API compatibility layer, MCP tools
**Storage**: SQLModel/PostgreSQL for backend persistence
**Testing**: pytest for backend, Jest/React Testing Library for frontend
**Target Platform**: Web application with Next.js frontend and FastAPI backend
**Project Type**: Web
**Performance Goals**: Sub-second response times for chat interactions
**Constraints**: Must maintain JWT authentication security, preserve existing functionality
**Scale/Scope**: Individual user isolation maintained, multi-language support for English, Urdu, and major languages

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
specs/4-remove-user-id-prompt-lang-match/
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
│   │   ├── chat_routes.py          # Chat API endpoint (where context injection happens)
│   │   └── task_routes.py          # Task API endpoints
│   ├── mcp/
│   │   └── tools.py                # MCP tools that need user_id injection wrapper
│   ├── middleware/
│   │   └── auth.py                 # JWT authentication middleware
│   └── services/
│       └── chat_service.py         # Chat service logic
└── tests/

frontend/
├── src/
│   ├── components/
│   │   ├── AIChat.tsx              # Chat UI component
│   │   ├── ChatKit/
│   │   │   └── ChatKit.tsx         # Enhanced chat UI component
│   │   └── GlassCard.tsx           # UI components with glassmorphism
│   ├── app/
│   │   └── tasks/
│   │       └── page.tsx            # Tasks page
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
| Modifying existing tool signatures | Need to wrap tools with user_id injection | Direct modification would break existing contracts |