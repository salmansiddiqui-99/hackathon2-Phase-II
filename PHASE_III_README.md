# Phase III - AI Agent & ChatKit Integration

This is the third phase of the Todo Fullstack Web Application featuring AI Agent integration and ChatKit frontend. This phase implements an intelligent AI assistant that can manage tasks using natural language processing.

## Features

- **AI-Powered Task Management**: Interact with tasks using natural language
- **9-Step Stateless Conversation Flow**: Robust stateless conversation handling
- **MCP Tool Integration**: Uses Model Context Protocol for task operations
- **Secure Authentication**: JWT-based authentication with user isolation
- **ChatKit Frontend**: Modern chat interface for AI interactions
- **Task Operations**: Complete CRUD operations with confirmation flows

## Architecture

### Backend Components

1. **AI Agent** (`backend/src/ai/agent.py`):
   - Processes natural language requests
   - Orchestrates MCP tools for task operations
   - Handles confirmation flows for critical operations
   - Implements safety checks and error handling

2. **AI Service** (`backend/src/services/ai_service.py`):
   - Implements the 9-step stateless conversation flow
   - Manages conversation state and history
   - Coordinates between chat service and AI agent

3. **MCP Tools** (`backend/src/mcp/tools.py`):
   - `add_task`: Create new tasks
   - `list_tasks`: Retrieve all user tasks
   - `complete_task`: Mark tasks as completed
   - `delete_task`: Remove tasks with confirmation
   - `update_task`: Modify task details

4. **Chat Service** (`backend/src/services/chat_service.py`):
   - Manages conversation persistence
   - Ensures user isolation
   - Handles message history

### Frontend Components

1. **ChatKit Component** (`frontend/src/components/ChatKit/ChatKit.tsx`):
   - Modern chat interface
   - JWT authentication integration
   - Real-time message handling

2. **Chat Page** (`frontend/src/app/chat/page.tsx`):
   - Main chat interface
   - Protected route implementation

## 9-Step Stateless Conversation Flow

The system implements a 9-step conversation flow to ensure proper state management:

1. **Validate Input**: Validates user input and authentication
2. **Retrieve History**: Fetches conversation history from database
3. **Save User Message**: Stores the user's message in the conversation
4. **Process with AI**: Sends request to AI agent for processing
5. **Execute Tool Calls**: Runs any required MCP tool operations
6. **Generate Response**: Creates final response from AI
7. **Save Assistant Reply**: Stores AI's response in conversation
8. **Update Conversation**: Updates conversation metadata
9. **Return Result**: Sends response back to client

## Task Operations

### Add Task
- Natural language: "Add a task to buy groceries"
- Creates new task with title and optional description

### List Tasks
- Natural language: "What tasks do I have?"
- Returns all user's tasks

### Complete Task
- Natural language: "Mark my grocery task as completed"
- Updates task completion status

### Delete Task
- Natural language: "Delete my meeting task"
- Requires explicit user confirmation before deletion
- Asks: "Are you sure you want to delete the task?" before proceeding

### Update Task
- Natural language: "Update my meeting task to tomorrow"
- Modifies task details with confirmation for major changes

## Security Features

- **User Isolation**: Each user can only access their own tasks
- **JWT Authentication**: Secure token-based authentication
- **Input Validation**: Comprehensive input sanitization
- **Rate Limiting**: Built-in rate limiting for API protection

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL (or NeonDB for cloud deployment)

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your OpenRouter API key
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Environment Variables

Create `.env` files in both backend and frontend directories:

**Backend (.env)**:
```env
OPENROUTER_API_KEY=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
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Frontend (.env.local)**:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_OPENAI_API_KEY=your-openai-api-key  # Only if using real OpenAI ChatKit
```

## API Endpoints

- `POST /api/{user_id}/chat` - Chat with AI assistant
- `GET /api/{user_id}/conversations` - List user conversations
- `GET /api/{user_id}/conversations/{conversation_id}` - Get specific conversation
- `DELETE /api/{user_id}/conversations/{conversation_id}` - Delete conversation

## Error Handling

The system includes comprehensive error handling:

- API failures are gracefully handled with user-friendly messages
- Database connection issues are caught and logged
- Invalid requests are validated and rejected
- Token expiration is properly handled

## Testing

To test the AI functionality:

1. Start the backend server: `uvicorn backend.src.main:app --reload`
2. Navigate to the chat page in the frontend
3. Try natural language commands:
   - "Add a task to water the plants"
   - "Show me my tasks"
   - "Complete task 1"
   - "Delete my shopping task" (will ask for confirmation)

## Production Considerations

- Configure domain allowlist for ChatKit in production
- Implement proper monitoring and logging
- Set up rate limiting appropriately
- Ensure SSL/TLS for all connections
- Regular security audits of AI prompts

## Technologies Used

- **Backend**: FastAPI, SQLModel, PostgreSQL
- **AI**: OpenAI-compatible API (via OpenRouter)
- **Frontend**: Next.js, React, TypeScript
- **Authentication**: JWT tokens
- **Tools**: MCP (Model Context Protocol)

## License

MIT License - See LICENSE file for details.