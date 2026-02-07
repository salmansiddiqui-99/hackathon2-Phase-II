from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth_router, task_router, chat_router
from .api.conversation_routes import router as conversation_router
from .middleware.auth import jwt_middleware
from .logging_config import logger
from .rate_limiter import setup_rate_limiter, limiter
from slowapi.errors import RateLimitExceeded
from .performance_monitor import PerformanceMonitoringMiddleware
from .mcp.server import get_mcp_server
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Todo API", version="1.0.0")

# Add CORS middleware FIRST to handle preflight requests properly
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://localhost:8080",  # Common alternative port
        "http://127.0.0.1:8080",
    ],  # Specific origins for development
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],  # Explicitly allow methods
    allow_headers=["*"],  # Allow all headers including Authorization
    # Add exposed headers to make Authorization available to frontend
    expose_headers=["Access-Control-Allow-Origin", "Authorization"]
)

# Add JWT middleware for authentication
app.middleware('http')(jwt_middleware)

# Add performance monitoring middleware
app.add_middleware(PerformanceMonitoringMiddleware)

# Set up rate limiting
setup_rate_limiter(app)

# Include the routers
app.include_router(auth_router, prefix="/api", tags=["Authentication"])
app.include_router(task_router, prefix="/api", tags=["Tasks"])
app.include_router(chat_router, prefix="/api", tags=["Chat"])
app.include_router(conversation_router, prefix="/api", tags=["Conversations"])

@app.get("/")
def read_root():
    """
    Root endpoint for the API
    """
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Todo API"}

@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    logger.info("Health check endpoint accessed")
    return {"status": "healthy", "service": "todo-api"}


@app.get("/mcp/tools")
def get_mcp_tools():
    """
    Endpoint to retrieve available MCP tools for AI agents
    """
    logger.info("MCP tools endpoint accessed")
    server = get_mcp_server()
    tools_schemas = server.get_all_tools_schemas()
    return {"tools": tools_schemas}


@app.post("/mcp/tools/{tool_name}")
def call_mcp_tool(tool_name: str, params: dict):
    """
    Endpoint to call a specific MCP tool
    """
    logger.info(f"MCP tool {tool_name} called")
    server = get_mcp_server()
    result = server.call_tool(tool_name, params)
    return result