# Reusable Skill: AI Chatbot Agent Orchestrator

**Skill ID**: ai-chatbot-orchestrator
**Version**: 1.0
**Phase**: III (AI-Powered Todo Chatbot)
**Author**: Claude Code Subagent
**Bonus Category**: Reusable Intelligence (+200 points)

## Description
Reusable intelligence skill that creates a fully functional AI chatbot capable of managing todo tasks through natural language using OpenRouter + MCP tools.

## Capabilities
- Configures OpenRouter client (DeepSeek-R1T2-Chimera free model)
- Initializes OpenAI Agents SDK agent with MCP tool calling
- Enforces exact agent behavior rules from hackathon spec
- Orchestrates stateless chat endpoint with conversation persistence
- Integrates OpenAI ChatKit frontend with JWT authentication
- Supports multi-turn conversations with full context

## Invocation Examples

```markdown
@ai-chatbot-agent
Implement the full AI agent and /api/{user_id}/chat endpoint using OpenRouter configuration and MCP tools from @specs/mcp-tools.md".