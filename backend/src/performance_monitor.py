import time
import functools
from typing import Callable, Any
from .logging_config import logger
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class PerformanceMonitor:
    """Class to handle performance monitoring and optimization"""

    @staticmethod
    def log_execution_time(func: Callable) -> Callable:
        """Decorator to log execution time of functions"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

            execution_time = end_time - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.4f}s")

            return result
        return wrapper


class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware to monitor performance of API requests"""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        end_time = time.time()
        execution_time = end_time - start_time

        # Log performance metrics
        logger.info(
            f"Request: {request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Time: {execution_time:.4f}s | "
            f"IP: {request.client.host}"
        )

        # Add performance timing header (remove in production for security)
        response.headers["X-Response-Time"] = f"{execution_time:.4f}s"

        return response


def monitor_performance():
    """Initialize performance monitoring"""
    logger.info("Performance monitoring initialized")
    return PerformanceMonitor()