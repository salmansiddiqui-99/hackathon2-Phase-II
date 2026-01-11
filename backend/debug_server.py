#!/usr/bin/env python3
"""
Debug script to test the server startup and catch any errors
"""
import traceback
from src.main import app
import uvicorn

def test_imports():
    """Test individual imports to identify the issue"""
    print("Testing individual imports...")

    try:
        from src.api import auth_router, task_router
        print("[OK] Routers imported successfully")
    except Exception as e:
        print(f"[ERROR] Error importing routers: {e}")
        traceback.print_exc()
        return False

    try:
        from src.middleware.auth import jwt_middleware
        print("[OK] Auth middleware imported successfully")
    except Exception as e:
        print(f"[ERROR] Error importing auth middleware: {e}")
        traceback.print_exc()
        return False

    try:
        from src.logging_config import logger
        print("[OK] Logger imported successfully")
    except Exception as e:
        print(f"[ERROR] Error importing logger: {e}")
        traceback.print_exc()
        return False

    try:
        from src.rate_limiter import setup_rate_limiter, limiter
        print("[OK] Rate limiter imported successfully")
    except Exception as e:
        print(f"[ERROR] Error importing rate limiter: {e}")
        traceback.print_exc()
        return False

    return True

def test_auth_service():
    """Test authentication service specifically"""
    print("\nTesting authentication service...")

    try:
        from src.services.auth_service import AuthService
        print("[OK] AuthService imported successfully")
    except Exception as e:
        print(f"[ERROR] Error importing AuthService: {e}")
        traceback.print_exc()
        return False

    try:
        from src.models import User
        print("[OK] User model imported successfully")
    except Exception as e:
        print(f"[ERROR] Error importing User model: {e}")
        traceback.print_exc()
        return False

    return True

def test_server_startup():
    """Test server startup without running it"""
    print("\nTesting server startup...")

    try:
        # Just test creating the app without running
        app_instance = app  # This is the imported app
        print(f"[OK] App created successfully: {type(app_instance)}")

        # Check if routes are registered
        routes = [route.path for route in app_instance.routes]
        print(f"[OK] Routes registered: {len(routes)} routes")
        print(f"  Paths: {routes[:5]}{'...' if len(routes) > 5 else ''}")

    except Exception as e:
        print(f"[ERROR] Error creating app: {e}")
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    print("Starting debug tests...\n")

    success = True
    success &= test_imports()
    success &= test_auth_service()
    success &= test_server_startup()

    if success:
        print("\n[OK] All tests passed! The server should work.")
    else:
        print("\n[ERROR] Some tests failed. Please check the errors above.")