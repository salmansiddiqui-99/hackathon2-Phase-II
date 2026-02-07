# Implementation Plan: AI Agent & ChatKit Integration

**Feature**: AI Agent & ChatKit Integration
**Branch**: 3-ai-agent-chatkit
**Created**: 2026-01-22
**Status**: Draft

## Technical Context

Based on analysis of the existing codebase:

- **Backend Framework**: FastAPI with SQLModel and existing authentication system
- **MCP Tools**: Already implemented in `backend/src/mcp/` with five task tools
- **Authentication**: JWT-based using Better Auth with middleware protection
- **Existing API Structure**: `/api/{user_id}/chat` endpoint already implemented for stateless chat
- **Frontend**: Next.js application in `frontend/` directory
- **Requirements**: Need to add OpenAI Agents SDK and OpenRouter dependencies

**Architecture Components Identified**:
- OpenRouter configuration: API keys, base URLs, model selection
- AI Agent: Integration with OpenAI Agents SDK using MCP tools
- Chat orchestration: FastAPI endpoint → agent → MCP tools → response
- ChatKit frontend: OpenAI ChatKit UI configuration
- Authentication bridge: JWT token passing from frontend to backend

**NEEDS CLARIFICATION**: [None - all requirements understood from spec and codebase analysis]

## Constitution Check

✅ **Spec-Driven Development**: Following detailed specification from feature requirements
✅ **No Manual Coding**: Plan outlines code generation approach via Claude Code
✅ **Cloud-Native Focus**: Using OpenRouter for cloud-native AI processing
✅ **Stateless Design**: Aligns with requirement for stateless conversation flow
✅ **Multi-User Support**: Leverages existing JWT authentication and user isolation patterns
✅ **AI Integration**: Uses OpenAI Agents SDK and MCP tools as specified

## Gates

- [x] **Architecture Alignment**: Solution fits within existing FastAPI/Next.js architecture
- [x] **Security Compliance**: Plan maintains JWT authentication and user isolation requirements
- [x] **Technology Alignment**: Uses OpenAI Agents SDK and OpenRouter as required
- [x] **Scalability**: Stateless design supports horizontal scaling
- [x] **Constraint Compliance**: All agent operations go through MCP tools, no direct DB access

## Phase 0: Research & Discovery

### Research Summary

Based on codebase analysis, all architectural patterns are understood:

1. **Backend Integration**: Following existing `/api/{user_id}/chat` pattern for AI integration
2. **Authentication**: Reusing existing JWT middleware and dependency patterns
3. **MCP Tools**: Integrating with existing MCP tools from Part 2
4. **Frontend Integration**: Adding ChatKit UI following existing Next.js patterns

### Decision Log

- **Decision**: Use OpenRouter with specified configuration (API Key, Model, Base URL)
- **Rationale**: Required by specification and provides access to the specified model
- **Alternatives considered**: Direct OpenAI API (rejected - OpenRouter required by spec)

- **Decision**: Implement function calling for tool integration
- **Rationale**: Best practice for AI agent tool integration, allows parallel operations
- **Alternatives considered**: Custom API calls (rejected - function calling is standard)

- **Decision**: Maintain stateless operation with database-based state management
- **Rationale**: Consistent with existing stateless design requirement and existing chat implementation
- **Alternatives considered**: Server-side session storage (rejected - contradicts stateless requirement)

## Phase 1: Data Model & Contracts

### Data Model Design

#### AI Agent Request/Response Model
- **Input**: Natural language query from user with user_id and optional conversation_id
- **Output**: Structured response with conversation_id, response text, and any tool_calls
- **Tool Parameters**: MCP tool parameters following existing MCP tool specifications

### API Contract Design

#### POST /api/{user_id}/chat Endpoint (Enhanced)
The existing endpoint will be enhanced to route requests to the AI agent instead of simple stateless processing.

**Request Body**:
```json
{
  "conversation_id": "optional string",
  "message": "string - natural language query"
}
```

**Response**:
```json
{
  "conversation_id": "string",
  "response": "string - AI agent's response",
  "tool_calls": "array of tool call results"
}
```

### Quickstart Guide for Implementation

1. **Configure OpenRouter**: Set up OpenRouter API configuration with provided credentials
2. **Create AI Agent**: Initialize agent with OpenAI Agents SDK and MCP tools
3. **Engineer Prompts**: Create system prompt with exact agent behavior rules
4. **Orchestrate Chat**: Connect FastAPI endpoint → agent → MCP tools → response
5. **Configure ChatKit**: Set up OpenAI ChatKit UI to connect to backend
6. **Bridge Authentication**: Ensure JWT tokens pass correctly from frontend to backend
7. **Test Implementation**: Validate all natural language commands work correctly

## Phase 2: Implementation Approach

### Component Creation Plan

1. **OpenRouter Configuration** (`backend/src/ai/openrouter_config.py`)
   - Set up base_url, api_key, and model configuration
   - Create client for OpenRouter API

2. **AI Agent Initialization** (`backend/src/ai/agent.py`)
   - Create agent with OpenAI Agents SDK
   - Integrate with existing MCP tools
   - Implement tool registration and calling

3. **Prompt Engineering** (`backend/src/ai/prompt.py`)
   - Create system prompt with exact agent behavior rules
   - Define task operation instructions
   - Include error handling guidelines

4. **Chat Orchestration** (`backend/src/api/chat_routes.py` - enhanced)
   - Enhance existing `/api/{user_id}/chat` endpoint
   - Route requests to AI agent
   - Process agent responses and tool calls

5. **ChatKit Frontend Configuration** (`frontend/src/components/ChatKit.tsx` or similar)
   - Configure OpenAI ChatKit UI
   - Connect to backend endpoint
   - Handle authentication tokens

6. **Authentication Bridge** (`frontend/src/lib/auth.ts` or similar)
   - Ensure JWT tokens are passed from ChatKit to backend
   - Configure domain allowlist for production

### Development Sequence

1. **OpenRouter Config**: Set up the OpenRouter client configuration
2. **AI Agent**: Create the agent with MCP tool integration
3. **Prompt Engineering**: Define the system behavior rules
4. **Chat Enhancement**: Enhance existing chat endpoint to use AI agent
5. **Frontend**: Configure ChatKit UI to connect to backend
6. **Auth Bridge**: Ensure proper JWT token flow between frontend and backend
7. **Testing**: Validate all natural language commands work correctly

## Phase 3: Validation Strategy

### Testing Approach

1. **Unit Tests**: Test individual AI agent functions and tool calls
2. **Integration Tests**: Test AI agent with MCP tools integration
3. **End-to-End Tests**: Full flow testing with ChatKit UI

### Validation Checks

1. **Add task command**: "Add task buy milk" → task created via MCP tools
2. **List tasks command**: "List my tasks" → returns current tasks via MCP tools
3. **Complete task command**: "Mark task 1 as done" → status updated via MCP tools
4. **Delete task command**: "Delete task 3" → removed via MCP tools
5. **Update task command**: "Update task 2 title to groceries" → changed via MCP tools
6. **Wrong command**: "Invalid command" → helpful error message
7. **Multi-turn conversation**: Context preservation across multiple exchanges

### Test Tools

- ChatKit UI for manual testing
- Direct API calls for automated testing
- Existing test infrastructure in `backend/tests/`

## Risk Analysis

### Primary Risks

1. **API Limitations**: OpenRouter API rate limits or availability issues
   - *Mitigation*: Implement proper error handling and retry logic

2. **Natural Language Understanding**: AI agent may misinterpret commands
   - *Mitigation*: Comprehensive prompt engineering and error handling

3. **Authentication Flow**: Issues with JWT token passing between ChatKit and backend
   - *Mitigation*: Proper authentication bridge implementation and testing

### Backup Strategies

- Fallback plan: Maintain original chat functionality if AI integration fails
- Monitoring: Log all AI interactions for debugging
- Validation: Extensive testing of natural language commands before deployment

## Success Criteria

- [ ] OpenRouter configured with specified API Key, Model, and Base URL
- [ ] AI agent created with OpenAI Agents SDK and MCP tool integration
- [ ] System prompt engineered with exact agent behavior rules
- [ ] Chat orchestration connects endpoint → agent → MCP tools → response
- [ ] ChatKit UI configured and connected to backend
- [ ] Authentication bridge passes JWT tokens correctly
- [ ] All natural language commands work reliably (90%+ success rate)
- [ ] User isolation maintained with 100% accuracy
- [ ] Stateless conversation flow operates correctly