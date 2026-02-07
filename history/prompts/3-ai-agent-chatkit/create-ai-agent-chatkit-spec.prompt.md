---
id: 9
title: create-ai-agent-chatkit-spec
stage: spec
date: 2026-01-22
surface: agent
model: claude-opus-4-5-20251101
feature: ai-agent-chatkit
branch: 3-ai-agent-chatkit
user: haroon traders
command: /sp.specify
labels: [specification, ai-agent, chatkit, openrouter, natural-language]
links:
  spec: specs/3-ai-agent-chatkit/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/3-ai-agent-chatkit/spec.md
 - specs/3-ai-agent-chatkit/checklists/requirements.md
tests:
 - specs/3-ai-agent-chatkit/spec.md validated against requirements checklist
---

## Prompt

Phase III - Part 3: AI Agent & ChatKit Integration

Target audience: Hackathon participants and judges evaluating AI chatbot capabilities
Focus: Creating the AI agent using OpenRouter and integrating OpenAI ChatKit frontend with natural language understanding

Success criteria:
- AI Agent built with OpenAI Agents SDK (compatible with OpenRouter)
- Uses OpenRouter configuration:
  - API Key: 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
  - Model: tngtech/deepseek-r1t2-chimera:free
  - Base URL: https://openrouter.ai/api/v1
- Agent follows exact Agent Behavior Specification (task creation, listing, completion, deletion, update, confirmation, error handling)
- Understands natural language commands from the hackathon examples
- Integrates with MCP tools from Part 2
- Frontend: OpenAI ChatKit UI connected to POST /api/{user_id}/chat
- Conversation flow: 9-step stateless cycle fully implemented
- Maintains all Basic Level functionality through natural language

Constraints:
- All LLM calls must go through OpenRouter with the provided key/model/base_url
- Agent must use MCP tools – no direct DB or API calls
- ChatKit must be configured with domain allowlist for production
- Use existing Phase II auth (JWT) for ChatKit → backend calls
- Generate via Claude Code only

Not building:
- Intermediate or Advanced Level features
- Voice input or multi-language support
- Deployment to Kubernetes (Phase IV)
- Kafka/Dapr integration

## Response snapshot

Created a comprehensive specification for the AI Agent & ChatKit Integration feature. The specification includes:

- User scenarios for natural language task management, AI-powered task operations, and secure AI integration
- Functional requirements covering OpenAI Agents SDK integration, OpenRouter configuration, natural language processing, MCP tool integration, and ChatKit UI connection
- Key entities (AI Agent, ChatKit UI, OpenRouter Connection, MCP Tools) with their roles
- Success criteria with measurable outcomes for accuracy, reliability, security, and performance

The specification is ready for the planning phase and follows the Agentic Dev Stack approach with focus on natural language interaction and AI-powered task management.

## Outcome

- ✅ Impact: Created complete feature specification with user scenarios, requirements and success criteria for AI agent integration
- 🧪 Tests: Specification validated against requirements checklist with all items completed
- 📁 Files: Created spec.md and requirements checklist in specs/3-ai-agent-chatkit/
- 🔁 Next prompts: Ready for /sp.plan to design the implementation architecture
- 🧠 Reflection: Specification addresses all core requirements from the user input with appropriate user stories and testable requirements

## Evaluation notes (flywheel)

- Failure modes observed: None - specification completed successfully
- Graders run and results (PASS/FAIL): PASS - all checklist items validated
- Prompt variant (if applicable): Standard /sp.specify command
- Next experiment (smallest change to try): Proceed to /sp.plan for architectural design