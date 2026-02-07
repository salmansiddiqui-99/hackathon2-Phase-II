from .auth_routes import router as auth_router
from .task_routes import router as task_router
from .chat_routes import router as chat_router

__all__ = ["auth_router", "task_router", "chat_router"]