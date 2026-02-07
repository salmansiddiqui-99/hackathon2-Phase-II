# Implementation Plan: Switch LLM Provider from OpenRouter to Cohere (Free Trial Tier)

**Feature**: Switch LLM Provider from OpenRouter to Cohere (Free Trial Tier)
**Branch**: 001-switch-llm-provider
**Created**: 2026-02-04
**Status**: Planned

## Overview

This plan outlines the implementation steps to replace the OpenRouter-based LLM configuration with Cohere's free Trial API key using the OpenAI-compatible Compatibility API layer, while preserving all Phase III functionality (MCP tools, stateless chat endpoint, agent behavior, ChatKit integration).

## Architectural Decisions

### 1. Base URL Selection
- **Decision**: Use `https://api.cohere.ai/compatibility/v1` as the Cohere compatibility endpoint
- **Rationale**: Official Cohere OpenAI Compatibility API endpoint confirmed in 2026 documentation
- **Impact**: Enables seamless integration with existing OpenAI SDK infrastructure

### 2. Model Selection
- **Decision**: Use `command-r7b-12-2024` for initial implementation
- **Rationale**: Offers lowest latency and highest trial tolerance compared to larger models
- **Trade-offs**: Smaller model may have slightly reduced reasoning capability but better trial usage characteristics

### 3. API Key Handling
- **Decision**: Configure the provided trial key in environment variables with `.env` file approach
- **Rationale**: Maintains security best practices while allowing easy key rotation
- **Implementation**: Store in `.env` file and load via existing `dotenv` pattern

### 4. Fallback Strategy
- **Decision**: Single-model approach with documentation of manual switchover if trial quota exhausted
- **Rationale**: Simplifies implementation while meeting trial-based usage constraints

## Implementation Steps

### Phase 1: Client Configuration Update

**Objective**: Update AsyncOpenAI client initialization with Cohere compatibility settings

#### Tasks:
1. Modify `backend/src/ai/openrouter_config.py` or create new `cohere_config.py`:
   - Replace OpenRouter client setup with Cohere-compatible AsyncOpenAI client
   - Set base URL to `https://api.cohere.ai/compatibility/v1`
   - Configure API key with provided trial key: `SqnhRaifcIHJyGeTqODA955lm5VvIlP1cJHYtDmM`

2. Update environment configuration:
   - Add COHERE_API_KEY to `.env.example`
   - Update `.env` file with the trial key

#### Dependencies:
- None

#### Success Criteria:
- AsyncOpenAI client successfully initialized with Cohere settings
- Client can connect to Cohere API endpoint

### Phase 2: Model Configuration Update

**Objective**: Select and configure a free-tier eligible Cohere model

#### Tasks:
1. Update model selection in agent configuration:
   - Set model name to `command-r7b-12-2024`
   - Ensure model compatibility with OpenAI SDK tool-calling features

2. Update model configuration in `backend/src/ai/agent.py`:
   - Integrate Cohere model with existing OpenAIChatCompletionsModel pattern
   - Verify tool-calling compatibility with Cohere's implementation

#### Dependencies:
- Phase 1 completion

#### Success Criteria:
- Cohere model successfully configured and recognized by OpenAI SDK
- Model supports required tool-calling functionality

### Phase 3: RunConfig Update

**Objective**: Adjust RunConfig to use the new Cohere-compatible model and client

#### Tasks:
1. Update `RunConfig` in `backend/src/ai/agent.py`:
   - Point to the new Cohere-compatible model
   - Use the Cohere AsyncOpenAI client as the provider
   - Maintain existing tracing and other configuration settings

2. Verify configuration compatibility:
   - Test that RunConfig can be instantiated with Cohere client
   - Confirm all required parameters are properly set

#### Dependencies:
- Phase 1 and 2 completion

#### Success Criteria:
- RunConfig successfully initializes with Cohere configuration
- No runtime errors when creating RunConfig instances

### Phase 4: Agent Preservation

**Objective**: Maintain existing Agent definition, system instructions, and MCP tool bindings

#### Tasks:
1. Preserve existing agent configuration:
   - Keep existing system instructions intact
   - Maintain all MCP tool definitions and bindings
   - Verify that tool schemas remain compatible

2. Test agent functionality:
   - Confirm that existing Agent behavior is preserved
   - Verify tool-calling workflows continue to work as expected

#### Dependencies:
- Phase 3 completion

#### Success Criteria:
- Agent maintains identical behavior to OpenRouter implementation
- All existing MCP tools function properly

### Phase 5: Endpoint Adjustment

**Objective**: Tweak chat orchestration if needed to handle differences in Cohere's responses

#### Tasks:
1. Review chat endpoint for Cohere compatibility:
   - Adjust for potential differences in tool-call format
   - Handle any variations in response structure
   - Update error handling for Cohere-specific responses

2. Update `backend/src/api/chat_routes.py` if needed:
   - Make minor adjustments to accommodate Cohere response format
   - Ensure error handling covers Cohere-specific error conditions

#### Dependencies:
- Phase 4 completion

#### Success Criteria:
- Chat endpoint handles Cohere responses correctly
- Tool calls are properly parsed and executed

### Phase 6: Documentation Update

**Objective**: Add documentation about Cohere Trial switch and usage limits

#### Tasks:
1. Update README with Cohere-specific information:
   - Explain why Cohere Trial was chosen (cost optimization)
   - Document trial limitations (~1,000 calls/month, 20 chat/min)
   - Provide usage guidelines for demo purposes

2. Update `CLAUDE.md` with implementation notes:
   - Document Cohere Trial integration
   - Note trial usage constraints
   - Reference implementation rationale

#### Dependencies:
- All previous phases completed

#### Success Criteria:
- Documentation clearly explains Cohere integration
- Users understand trial limitations and usage guidelines

## Technical Approach

### Compatibility Strategy
- Leverage Cohere's OpenAI Compatibility API for minimal code changes
- Maintain existing OpenAI Agents SDK patterns
- Preserve MCP tool configurations without modification

### Risk Mitigation
- Conduct thorough testing of tool-calling functionality
- Implement graceful error handling for API quota limits
- Document fallback procedures if trial quota is exhausted

## Testing Strategy

### Validation Checks
1. **Task Creation**: Send "Add task buy milk tomorrow" → confirm task created via MCP tool
2. **Task Listing**: "List my tasks" → returns correct list
3. **Task Completion**: "Mark first task complete" → status updated
4. **Multi-turn Context**: Follow-up questions should maintain conversation context
5. **Rate Limit Awareness**: Ensure demo usage respects trial constraints (<20 calls/min)
6. **Response Quality**: Compare response quality and speed vs previous OpenRouter setup

### Testing Methodology
- Primary: ChatKit UI tests for end-to-end functionality
- Secondary: Log API calls to verify Cohere endpoint usage
- Monitor: Track API quota usage to stay within trial limits

## Success Metrics

1. **Functional Continuity**: 100% of existing chatbot interactions work identically
2. **Tool Integration**: All MCP tools (add_task, list_tasks, etc.) function properly
3. **Security Preservation**: User isolation mechanisms continue to work properly
4. **API Connection**: Successful requests processed through Cohere's compatibility endpoint
5. **Trial Compliance**: Adherence to trial usage constraints (20 req/min, 1000 calls/month)
6. **Behavior Consistency**: Natural language understanding remains consistent

## Rollback Plan

If issues arise during implementation:
1. Revert client configuration to OpenRouter settings
2. Restore previous model and RunConfig settings
3. Update environment variables back to OpenRouter configuration
4. Verify functionality with original OpenRouter setup

## Notes

- This implementation follows a minimal invasive change approach - only client/model configuration is swapped
- All existing business logic, database models, and security measures remain unchanged
- The Cohere compatibility layer should maintain full OpenAI SDK functionality including tool calling
- Trial usage constraints are appropriate for development and demo purposes