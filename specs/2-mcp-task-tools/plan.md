# Implementation Plan: MCP Server & Task Tools

**Feature**: MCP Server & Task Tools
**Branch**: 2-mcp-task-tools
**Created**: 2026-01-22
**Status**: Draft

## Technical Context

Based on analysis of the existing codebase:

- **Backend Framework**: FastAPI with SQLModel and Neon PostgreSQL
- **Database Models**: Task model already exists in `backend/src/models/task.py`
- **Services**: TaskService in `backend/src/services/` with existing operations
- **Authentication**: JWT-based using Better Auth with user_id validation
- **Database**: SQLModel with session management in `backend/src/database.py`

**Architecture Components Identified**:
- Models: Located in `backend/src/models/` (SQLModel classes)
- Services: Located in `backend/src/services/` (business logic)
- MCP Server: Needs to be created as a separate component or mounted app
- Database: SQLModel with session management in `backend/src/database.py`

**NEEDS CLARIFICATION**: [None - all requirements understood from spec and codebase analysis]

## Constitution Check

✅ **Spec-Driven Development**: Following detailed specification from feature requirements
✅ **No Manual Coding**: Plan outlines code generation approach via Claude Code
✅ **Cloud-Native Focus**: Using Neon PostgreSQL for cloud-native database
✅ **Stateless Design**: Aligns with requirement for stateless tool operations
✅ **Multi-User Support**: Leverages existing user isolation patterns
✅ **Reusable Intelligence**: MCP tools represent reusable intelligence for AI agents

## Gates

- [x] **Architecture Alignment**: Solution fits within existing FastAPI/SQLModel architecture
- [x] **Security Compliance**: Plan maintains user isolation and authentication requirements
- [x] **Technology Alignment**: Uses Official MCP SDK as required
- [x] **Scalability**: Stateless design supports horizontal scaling
- [x] **Constraint Compliance**: All tools will enforce no direct database access from agents

## Phase 0: Research & Discovery

### Research Summary

Based on codebase analysis, all architectural patterns are understood:

1. **Database Models**: Following existing Task model patterns with SQLModel
2. **Service Layer**: Reusing existing TaskService patterns with user_id validation
3. **Authentication**: Reusing existing JWT validation patterns
4. **MCP SDK**: Need to research Official MCP SDK integration patterns

### Decision Log

- **Decision**: Use Official MCP SDK for server implementation
- **Rationale**: Required by specification and part of Agentic Dev Stack principles
- **Alternatives considered**: Custom tool protocols (rejected - MCP SDK required)

- **Decision**: Implement tools as stateless operations reading/writing directly to DB
- **Rationale**: Consistent with stateless design requirement and existing patterns
- **Alternatives considered**: Caching layer (rejected - contradicts stateless requirement)

- **Decision**: Separate FastAPI app or mount for MCP server
- **Rationale**: Keeps MCP tools separate from main API while allowing shared resources
- **Alternatives considered**: Same app integration (rejected - separation of concerns)

## Phase 1: Data Model & Contracts

### Data Model Design

#### Task Model (Reused)
- **Reusing existing model**: `backend/src/models/task.py`
- **Fields**: id, user_id, title, description, completed, created_at, updated_at
- **Validation**: Title (1-255 chars), Description (0-1000 chars), completed (boolean)

### API Contract Design

#### MCP Tool Specifications

**add_task Tool**
```python
Parameters:
- user_id: int (required) - ID of the user creating the task
- title: str (required) - Title of the task (1-255 characters)
- description: str (optional) - Description of the task (0-1000 characters)

Returns:
- task_id: int - ID of the created task
- status: str - Status of the operation ("success" or error code)
- title: str - Title of the created task
```

**list_tasks Tool**
```python
Parameters:
- user_id: int (required) - ID of the user whose tasks to list

Returns:
- Array of tasks with:
  - id: int
  - title: str
  - description: str
  - completed: bool
  - created_at: datetime
  - updated_at: datetime
```

**complete_task Tool**
```python
Parameters:
- user_id: int (required) - ID of the user owning the task
- task_id: int (required) - ID of the task to complete

Returns:
- task_id: int - ID of the completed task
- status: str - Status of the operation ("success" or error code)
- title: str - Title of the completed task
```

**delete_task Tool**
```python
Parameters:
- user_id: int (required) - ID of the user owning the task
- task_id: int (required) - ID of the task to delete

Returns:
- task_id: int - ID of the deleted task
- status: str - Status of the operation ("success" or error code)
- title: str - Title of the deleted task
```

**update_task Tool**
```python
Parameters:
- user_id: int (required) - ID of the user owning the task
- task_id: int (required) - ID of the task to update
- title: str (optional) - New title for the task
- description: str (optional) - New description for the task
- completed: bool (optional) - New completion status

Returns:
- task_id: int - ID of the updated task
- status: str - Status of the operation ("success" or error code)
- title: str - Title of the updated task
```

### Quickstart Guide for Implementation

1. **Install MCP SDK**: Add Official MCP SDK to requirements
2. **Create MCP Server**: Set up new FastAPI app for MCP tools
3. **Implement Tools**: Create the five required tools with user_id validation
4. **Integrate with DB**: Use existing database connection and models
5. **Test Implementation**: Verify all tools work with proper user isolation
6. **Error Handling**: Ensure consistent error responses

## Phase 2: Implementation Approach

### Component Creation Plan

1. **MCP Server Setup** (`backend/src/mcp_server.py` or similar)
   - Initialize Official MCP SDK server
   - Configure as separate app or mounted route
   - Set up shared database connection

2. **Tool Definitions** (`backend/src/mcp_tools.py` or similar)
   - Define the 5 required tools using MCP SDK
   - Implement proper input validation with Pydantic models
   - Ensure consistent return formats

3. **Tool Implementation** (`backend/src/mcp_tools.py`)
   - add_task: Create new task with user_id validation
   - list_tasks: Return all tasks for user_id
   - complete_task: Update task completion status with user validation
   - delete_task: Remove task with user validation
   - update_task: Update task fields with user validation

4. **Ownership Enforcement** (`backend/src/mcp_tools.py`)
   - Validate user_id matches task owner in all operations
   - Return appropriate errors for unauthorized access

5. **Error Handling** (`backend/src/mcp_tools.py`)
   - Implement consistent error response format
   - Handle database connection failures gracefully
   - Validate all input parameters

### Development Sequence

1. **MCP Setup First**: Create the MCP server infrastructure
2. **Tool Definitions**: Define the tool signatures and validation
3. **Individual Tools**: Implement each tool with proper validation
4. **Integration**: Connect to existing database and models
5. **Testing**: Verify all tools work with proper security

## Phase 3: Validation Strategy

### Testing Approach

1. **Unit Tests**: Test individual tool functions
2. **Integration Tests**: Test MCP server with mocked database
3. **End-to-End Tests**: Full flow testing with real database

### Validation Checks

1. **Call each tool with valid user_id**: Verify correct DB change occurs
2. **Call with wrong user_id**: Verify permission denied/empty result
3. **List after add**: Verify new task appears in list
4. **Complete operation**: Verify status toggles correctly
5. **Cross-user isolation**: Verify users can't access each other's tasks

### Test Tools

- Direct MCP tool calls via test client
- Database verification for state changes
- User isolation validation

## Risk Analysis

### Primary Risks

1. **Security Vulnerabilities**: Improper user isolation could expose tasks
   - *Mitigation*: Strict user_id validation in all tools

2. **MCP SDK Integration**: Potential compatibility issues with Official SDK
   - *Mitigation*: Thorough testing and validation of MCP integration

3. **State Management**: Ensuring truly stateless operation across all tools
   - *Mitigation*: All operations read/write directly from database

### Backup Strategies

- Rollback plan: Remove MCP server if integration issues arise
- Monitoring: Log all tool operations for debugging
- Validation: Extensive input validation to prevent injection attacks

## Success Criteria

- [ ] MCP server created using Official MCP SDK
- [ ] Five required tools implemented with proper validation
- [ ] User ownership enforced in all operations
- [ ] Consistent return formats across all tools
- [ ] Stateless operation maintained (no server-side storage)
- [ ] All validation checks pass
- [ ] User isolation maintained with 100% accuracy