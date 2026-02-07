# ADR 001: Switch from OpenRouter to Cohere Trial API for Cost Optimization

**Date**: 2026-02-04
**Status**: Accepted
**Authors**: Claude Code Assistant

## Context

The current Phase III AI-powered Todo application uses OpenRouter as its LLM provider with a paid tier. For development and demonstration purposes during the hackathon, we need a cost-effective solution that maintains the same functionality while minimizing expenses.

The application currently uses OpenAI Agents SDK with an AsyncOpenAI client configured for OpenRouter's DeepSeek model. We need to preserve all existing functionality including:
- MCP tools integration (add_task, list_tasks, complete_task, delete_task, update_task)
- Stateless chat endpoint with conversation history
- Multi-turn conversation context
- User isolation and security measures
- Natural language understanding for todo operations

## Decision

We will switch from OpenRouter to Cohere's Trial API using their OpenAI Compatibility layer. This approach:

1. Maintains all existing functionality with minimal code changes
2. Leverages Cohere's Command-R family models which are compatible with the free trial tier
3. Uses Cohere's OpenAI Compatibility API endpoint at `https://api.cohere.ai/compatibility/v1`
4. Implements the Cohere Trial API key: `SqnhRaifcIHJyGeTqODA955lm5VvIlP1cJHYtDmM`
5. Initially selects the `command-r7b-12-2024` model for optimal trial usage characteristics

## Alternatives Considered

### Continue with OpenRouter
- **Pros**: Already implemented, stable
- **Cons**: Incurs costs during development/demo, not ideal for hackathon budget constraints

### Switch to Native Cohere SDK
- **Pros**: Potentially better performance, Cohere-native features
- **Cons**: Requires significant refactoring of existing OpenAI Agents SDK integration, higher risk of breaking existing functionality

### Use OpenAI GPT models directly
- **Pros**: Similar to current pattern, reliable
- **Cons**: Would still incur costs unless using a specific free tier (which has limited availability)

## Rationale

The Cohere compatibility API approach offers the best balance of:
- Cost optimization (free trial tier for development/demo)
- Minimal implementation risk (preserves existing OpenAI SDK patterns)
- Feature parity (maintains all existing MCP tools and chat functionality)
- Trial usage constraints suitable for hackathon (1000 calls/month, 20/min rate limit)

## Implementation Details

1. Update the AsyncOpenAI client configuration in `backend/src/ai/agent.py`
2. Configure the Cohere compatibility endpoint and API key
3. Select an appropriate Command-R model for the trial tier
4. Verify all MCP tools continue to work with Cohere responses
5. Test multi-turn conversation context preservation

## Consequences

### Positive
- Significant cost reduction during development and demo phases
- Maintains full application functionality
- Easy rollback to previous provider if needed

### Negative
- Limited to trial usage constraints (1000 calls/month, 20/min rate limit)
- Potential vendor lock-in to Cohere API response formats
- Need to monitor usage to stay within trial limits

### Neutral
- Some response characteristics may vary slightly from OpenRouter implementation
- Documentation required to explain trial limitations

## Testing Strategy

- Validate all MCP tools continue to work with Cohere responses
- Confirm multi-turn conversation context is preserved
- Verify user isolation and security measures remain intact
- Test rate limit handling and error scenarios
- Ensure response quality meets application requirements