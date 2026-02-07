# Implementation Plan: Chat Database & Stateless Endpoint

**Feature**: Chat Database & Stateless Endpoint
**Branch**: 1-chat-database-stateless
**Created**: 2026-01-21
**Status**: Draft

## Technical Context

Based on analysis of the existing codebase:

- **Backend Framework**: FastAPI with SQLModel and Neon PostgreSQL
- **Authentication**: JWT-based using Better Auth with middleware protection
- **Existing Patterns**: User-specific routes with `{user_id}` in path, service layer architecture
- **Database Models**: SQLModel with base/read/create/update patterns
- **API Structure**: RESTful endpoints organized in routers with dependency injection

**Architecture Components Identified**:
- Models: Located in `backend/src/models/` (SQLModel classes)
- Services: Located in `backend/src/services/` (business logic)
- API Routes: Located in `backend/src/api/` (FastAPI routers)
- Authentication: JWT middleware in `backend/src/middleware/auth.py`
- Database: SQLModel with session management in `backend/src/database.py`

**NEEDS CLARIFICATION**: [None - all requirements understood from spec and codebase analysis]

## Constitution Check

✅ **Spec-Driven Development**: Following detailed specification from feature requirements
✅ **No Manual Coding**: Plan outlines code generation approach via Claude Code
✅ **Cloud-Native Focus**: Using Neon PostgreSQL for cloud-native database
✅ **Stateless Design**: Aligns with requirement for stateless implementation
✅ **Multi-User Support**: Leverages existing user isolation patterns
✅ **Authentication and Security**: Reuses JWT authentication patterns

## Gates

- [x] **Architecture Alignment**: Solution fits within existing FastAPI/SQLModel architecture
- [x] **Security Compliance**: Plan maintains user isolation and JWT protection
- [x] **Backward Compatibility**: All existing endpoints remain functional
- [x] **Technology Alignment**: Uses specified stack (SQLModel, Neon, JWT)
- [x] **Scalability**: Stateless design supports horizontal scaling

## Phase 0: Research & Discovery

### Research Summary

Based on codebase analysis, all architectural patterns are understood:

1. **Database Models**: Following existing Task/User model patterns with SQLModel
2. **API Routes**: Following existing `{user_id}` path parameter pattern
3. **Authentication**: Reusing existing JWT middleware and dependency patterns
4. **Service Layer**: Following existing service architecture in `src/services/`

### Decision Log

- **Decision**: Use SQLModel for database models following existing patterns
- **Rationale**: Consistent with existing codebase and Neon PostgreSQL support
- **Alternatives considered**: SQLAlchemy ORM (rejected - SQLModel already established)

- **Decision**: Implement JWT protection using existing middleware
- **Rationale**: Consistent with existing security patterns and user isolation
- **Alternatives considered**: Session-based auth (rejected - contradicts stateless requirement)

- **Decision**: Use `{user_id}/chat` route pattern matching existing API structure
- **Rationale**: Consistent with existing user-specific route patterns
- **Alternatives considered**: Different route structure (rejected - breaks consistency)

## Phase 1: Data Model & Contracts

### Data Model Design

#### Conversation Model
```python
class ConversationBase(SQLModel):
    """Base model for Conversation with common fields"""
    user_id: int = Field(index=True)  # Foreign key to user

class Conversation(ConversationBase, table=True):
    """Conversation model for database storage"""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation"""
    pass

class ConversationRead(ConversationBase):
    """Schema for reading a conversation with its ID"""
    id: int
    created_at: datetime
    updated_at: datetime
```

#### Message Model
```python
class MessageBase(SQLModel):
    """Base model for Message with common fields"""
    conversation_id: int = Field(index=True)  # Foreign key to conversation
    user_id: int = Field(index=True)  # Foreign key to user
    role: str = Field(regex="^(user|assistant)$", max_length=20)  # user or assistant
    content: str = Field(min_length=1, max_length=10000)  # Message content

class Message(MessageBase, table=True):
    """Message model for database storage"""
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MessageCreate(MessageBase):
    """Schema for creating a new message"""
    pass

class MessageRead(MessageBase):
    """Schema for reading a message with its ID"""
    id: int
    timestamp: datetime
```

### API Contract Design

#### POST /api/{user_id}/chat Endpoint
```yaml
paths:
  /api/{user_id}/chat:
    post:
      summary: Process chat message and return assistant response
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
          description: ID of the authenticated user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                conversation_id:
                  type: integer
                  nullable: true
                  description: Optional ID of existing conversation (creates new if not provided)
                message:
                  type: string
                  minLength: 1
                  maxLength: 10000
                  description: User's message content
              required:
                - message
      responses:
        '200':
          description: Successfully processed chat message
          content:
            application/json:
              schema:
                type: object
                properties:
                  conversation_id:
                    type: integer
                    description: ID of the conversation (newly created or existing)
                  response:
                    type: string
                    description: Assistant's response to the message
                  tool_calls:
                    type: array
                    items:
                      type: object
                    description: Any tool calls made by the assistant
                required:
                  - conversation_id
                  - response
        '401':
          description: Unauthorized - invalid or missing token
        '403':
          description: Forbidden - user attempting to access another user's conversations
        '422':
          description: Unprocessable Entity - validation error
```

### Quickstart Guide for Implementation

1. **Create Models**: Add Conversation and Message models to `backend/src/models/`
2. **Create Service**: Add ChatService with conversation/history/message logic
3. **Create Endpoint**: Add POST /api/{user_id}/chat route with JWT protection
4. **Update Dependencies**: Add new imports and register route in main app
5. **Test Implementation**: Verify all functionality with test cases

## Phase 2: Implementation Approach

### Component Creation Plan

1. **Database Models** (`backend/src/models/conversation.py`, `backend/src/models/message.py`)
   - Create Conversation and Message SQLModel classes
   - Define relationship between Conversation and Message
   - Include proper indexes and constraints

2. **Service Layer** (`backend/src/services/chat_service.py`)
   - Create ChatService with methods for:
     - Create/get conversation
     - Load conversation history
     - Save user/assistant messages
     - Process chat requests statelessly

3. **API Endpoint** (`backend/src/api/chat_routes.py`)
   - Create POST /api/{user_id}/chat endpoint
   - Validate JWT and user_id match
   - Handle optional conversation_id
   - Process message and return response

4. **Integration** (`backend/src/api/__init__.py`, `backend/src/main.py`)
   - Register new router in the API
   - Maintain backward compatibility

### Development Sequence

1. **Models First**: Create Conversation and Message models following existing patterns
2. **Service Layer**: Implement ChatService with database operations
3. **API Endpoint**: Create the chat endpoint with proper authentication
4. **Integration**: Connect everything and test

## Phase 3: Validation Strategy

### Testing Approach

1. **Unit Tests**: Test individual service methods
2. **Integration Tests**: Test API endpoints with mocked authentication
3. **End-to-End Tests**: Full flow testing with real authentication

### Validation Checks

1. **Create new conversation**: Send message without conversation_id → verify stored
2. **Continue conversation**: Send follow-up with same conversation_id → history preserved
3. **User isolation**: Different users → complete isolation
4. **Auth validation**: No token/invalid token → 401 error
5. **Stateless operation**: Multiple requests to different server instances → consistent results

### Test Tools

- Postman/curl for API testing
- Browser dev tools for debugging
- Existing test infrastructure in `backend/tests/`

## Risk Analysis

### Primary Risks

1. **Database Performance**: Large conversation histories could impact performance
   - *Mitigation*: Proper indexing and pagination for history retrieval

2. **Security Vulnerabilities**: Improper user isolation could expose conversations
   - *Mitigation*: Strict user_id validation in all endpoints

3. **State Management**: Ensuring truly stateless operation across server instances
   - *Mitigation*: All state retrieved from database, no server-side session storage

### Backup Strategies

- Rollback plan: Remove new endpoints/models if issues arise
- Monitoring: Log all chat operations for debugging
- Validation: Extensive input validation to prevent injection attacks

## Success Criteria

- [ ] Database models created following existing patterns
- [ ] API endpoint implements stateless design requirement
- [ ] JWT authentication properly integrated
- [ ] User isolation maintained with existing patterns
- [ ] Backward compatibility preserved
- [ ] All validation checks pass
- [ ] Performance meets requirements (<2s response time)