from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth_router, task_router
from .middleware.auth import jwt_middleware
from .logging_config import logger
from .rate_limiter import setup_rate_limiter, limiter
from slowapi.errors import RateLimitExceeded
from .performance_monitor import PerformanceMonitoringMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Todo API", version="1.0.0")

# Add JWT middleware for authentication
app.middleware('http')(jwt_middleware)

# Add performance monitoring middleware
app.add_middleware(PerformanceMonitoringMiddleware)

# Set up rate limiting
setup_rate_limiter(app)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(auth_router, prefix="/api", tags=["Authentication"])
app.include_router(task_router, prefix="/api", tags=["Tasks"])

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