# Feature Specification: Switch LLM Provider from OpenRouter to Cohere (Free Trial Tier)

**Feature Branch**: `001-switch-llm-provider`
**Created**: 2026-02-04
**Status**: Draft
**Input**: User description: "Phase III Extension: Switch LLM Provider from OpenRouter to Cohere (Free Trial Tier)

Target audience: Hackathon participants and judges evaluating flexibility in AI provider integration and cost-optimization strategies
Focus: Replace the OpenRouter-based LLM configuration (DeepSeek model) with Cohere's free Trial API key using the OpenAI-compatible Compatibility API layer, while preserving all Phase III functionality (MCP tools, stateless chat endpoint, agent behavior, ChatKit integration)

Success criteria:
- All LLM inference calls now route through Cohere's Compatibility API (OpenAI SDK compatible)
- Configuration uses provided Cohere Trial API key: SqnhRaifcIHJyGeTqODA955lm5VvIlP1cJHYtDmM
- Base URL set to Cohere's compatibility endpoint: https://api.cohere.com/v1 (or exact compatibility base as per latest docs)
- Use a strong free-tier-compatible chat model from Cohere's Command family, preferably:
  - command-r (if available in trial)
  - command-r-plus (if trial allows)
  - command-r7b (smaller/faster variant often more permissive in trial limits)
  - fallback to the most capable model explicitly allowed under trial restrictions
- Agent still uses OpenAI Agents SDK → configured with AsyncOpenAI client pointing to Cohere compatibility endpoint
- No change to MCP tools, database models, chat endpoint signature, or agent behavior rules
- Maintains exact natural language understanding and tool-calling behavior for Basic Level todo operations
- Trial usage constraints acknowledged (rate limits ~20 req/min chat, ~1,000 calls/month total – suitable for demo/hackathon testing)
- All code remains generated via Claude Code; no manual edits

Constraints:
- Must use Cohere **Trial** key only (free, evaluation/non-production)
- Cannot use paid/production Cohere keys or assume unlimited usage
- Keep OpenAI Agents SDK compatibility layer (AsyncOpenAI client + base_url override)
- Do NOT switch to native Cohere Python SDK unless Compatibility API fails – prefer OpenAI-style integration for minimal code changes
- Respect trial rate limits in demo (avoid high-frequency calls in video)
- No degradation of Phase III success criteria (multi-turn context, tool calling, user isolation)

Not building:
- Native Cohere SDK migration (cohere.ClientV2 / co.chat)
- Paid Cohere features or production-tier models
- New models outside Cohere's Command family
- Changes to Intermediate/Advanced features (still Basic Level only in Phase III)
- Reverting to direct OpenAI or other providers

Implementation guidance / rationale:
- Use pattern similar to provided example (AsyncOpenAI with custom base_url + api_key)
- Expected minimal change: replace base_url and api_key + select Cohere model name
- Document in CLAUDE.md or README why Cohere Trial was chosen (free vs. OpenRouter paid tiers)

This spec allows seamless provider swap while staying within hackathon constraints and leveraging Cohere's free trial for cost-free inference during development and demo."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Maintain Chat Functionality with New LLM Provider (Priority: P1)

As a user of the AI-powered todo application, I want the chatbot to continue working seamlessly after the LLM provider switch, so that I can interact with my todo lists naturally without noticing any difference in functionality.

**Why this priority**: This is the core functionality of the Phase III feature. Without this working, the entire AI chatbot capability would be broken, rendering the application unusable for its primary purpose.

**Independent Test**: Can be fully tested by verifying that all existing chatbot interactions (adding tasks, listing tasks, completing tasks, etc.) continue to work identically after the provider switch.

**Acceptance Scenarios**:

1. **Given** I am interacting with the AI chatbot, **When** I ask it to add a new task, **Then** it successfully adds the task to my list and confirms the action
2. **Given** I have tasks in my list, **When** I ask the chatbot to list my tasks, **Then** it returns all my tasks with correct details
3. **Given** I have tasks in my list, **When** I ask the chatbot to complete a specific task, **Then** it marks the task as completed and confirms the action

---

### User Story 2 - Preserve All AI Agent Behaviors and Tools (Priority: P1)

As a developer integrating this feature, I want the AI agent to continue using all existing MCP tools with identical behavior, so that no existing functionality is broken by the provider switch.

**Why this priority**: This ensures backward compatibility and prevents any disruption to the sophisticated tool-calling behaviors that were already implemented.

**Independent Test**: Can be fully tested by verifying that all MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) continue to work identically after the provider switch.

**Acceptance Scenarios**:

1. **Given** I am using the AI chatbot, **When** I request an action that requires tool calling, **Then** the appropriate tool is invoked and executes successfully
2. **Given** I have multiple tasks in my list, **When** I ask to update a specific task, **Then** the update_task tool is properly invoked and the task is updated

---

### User Story 3 - Configure New LLM Provider with Trial Account (Priority: P2)

As a developer implementing this change, I want to configure the AI agent to use Cohere's compatibility API with the provided trial key, so that we can leverage the free tier for development and demonstration purposes.

**Why this priority**: This is the core technical change required for the feature. It enables cost optimization while maintaining functionality.

**Independent Test**: Can be tested by verifying that LLM requests are successfully routed through Cohere's API endpoint with the provided API key and model.

**Acceptance Scenarios**:

1. **Given** the application is configured with Cohere credentials, **When** the AI agent makes an inference request, **Then** the request is processed through Cohere's API successfully
2. **Given** I am using the trial tier, **When** I make API requests, **Then** they respect the trial usage limits (~20 req/min, ~1000 calls/month)

---

### User Story 4 - Maintain User Isolation and Security (Priority: P1)

As a security-conscious user, I want my data to remain isolated from other users after the provider switch, so that my personal todo information remains private and secure.

**Why this priority**: This is a critical security requirement that must be maintained regardless of the underlying LLM provider.

**Independent Test**: Can be tested by verifying that users can only access their own conversations and tasks after the provider switch.

**Acceptance Scenarios**:

1. **Given** I am logged in as User A, **When** I access my conversations, **Then** I only see my own conversations and not those of User B
2. **Given** I am logged in as User A, **When** I try to access User B's data, **Then** the request is rejected with appropriate access controls

---

## Edge Cases

- What happens when the Cohere trial API key reaches its usage limits?
- How does the system handle network connectivity issues to Cohere's API?
- What happens when Cohere API returns unexpected responses or errors?
- How does the system handle rate limiting from Cohere's trial tier?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST route all LLM inference calls through Cohere's Compatibility API endpoint
- **FR-002**: System MUST use the provided Cohere Trial API key: SqnhRaifcIHJyGeTqODA955lm5VvIlP1cJHYtDmM
- **FR-003**: System MUST set the base URL to Cohere's compatibility endpoint: https://api.cohere.com/v1
- **FR-004**: System MUST use a Cohere Command family model (command-r, command-r-plus, or command-r7b) compatible with the free trial tier
- **FR-005**: System MUST continue using OpenAI Agents SDK with AsyncOpenAI client configured to point to Cohere endpoint
- **FR-006**: System MUST preserve all existing MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) without modification
- **FR-007**: System MUST maintain identical agent behavior rules and natural language understanding for todo operations
- **FR-008**: System MUST preserve all database models, chat endpoint signatures, and user isolation mechanisms
- **FR-009**: System MUST handle Cohere API errors gracefully and provide appropriate fallback responses
- **FR-010**: System MUST respect Cohere's trial usage constraints (approximately 20 requests/min chat, 1000 calls/month)

### Key Entities *(include if feature involves data)*

- **LLM Configuration**: Represents the LLM provider settings including API key, base URL, and model name
- **AI Agent**: Represents the AI-powered assistant that processes user requests and interacts with MCP tools
- **API Request**: Represents the data structure sent to the LLM provider for inference processing

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of existing chatbot interactions continue to work identically after the provider switch (no degradation in functionality)
- **SC-002**: All MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) are successfully invoked through the new provider
- **SC-003**: User isolation and security mechanisms continue to function properly (users only access their own data)
- **SC-004**: API requests are successfully processed through Cohere's compatibility endpoint with the provided credentials
- **SC-005**: Application demonstrates compliance with Cohere's trial usage constraints (respects rate limits and monthly quotas)
- **SC-006**: Natural language understanding and tool-calling behavior remains consistent with the original OpenRouter implementation
