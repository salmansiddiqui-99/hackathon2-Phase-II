from fastapi import Request, HTTPException, status
from typing import Callable, Awaitable
from ..auth import verify_token
import os
from dotenv import load_dotenv

load_dotenv()


async def jwt_middleware(request: Request, call_next: Callable) -> Awaitable:
    """
    Middleware to verify JWT tokens in the Authorization header
    """
    # Public routes that don't require authentication
    public_routes = [
        "/api/auth/register",
        "/api/auth/login",
        "/api/auth/logout",
        "/",
        "/health",
        "/docs",
        "/openapi.json",
        "/redoc"
    ]

    # Allow OPTIONS requests (preflight) to pass through for CORS
    if request.method == "OPTIONS":
        response = await call_next(request)
        return response

    # Allow public routes without token validation
    if request.url.path in public_routes:
        response = await call_next(request)
        return response

    # Extract the token from the Authorization header
    authorization_header = request.headers.get("Authorization")

    if not authorization_header:
        # For non-protected routes, allow the request to continue
        # Protected routes will handle the missing token in their dependencies
        response = await call_next(request)
        return response

    # Check if it starts with "Bearer "
    if not authorization_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format. Expected 'Bearer <token>'"
        )

    # Extract the actual token
    token = authorization_header[len("Bearer "):]

    # Verify the token
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # Add the user ID to the request state for use in route handlers
    user_id = payload.get("sub")  # Use "sub" as that's what's stored in the token
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user_id"
        )

    request.state.user_id = user_id
    response = await call_next(request)
    return response


def get_current_user_id(request: Request) -> str:
    """
    Helper function to get the current user ID from the request state
    This is meant to be used as a dependency in route handlers
    """
    if not hasattr(request.state, 'user_id'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in request state"
        )
    return request.state.user_id