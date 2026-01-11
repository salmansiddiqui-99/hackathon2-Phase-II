from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .logging_config import logger
from .auth import verify_token
import re
from urllib.parse import urlparse


class SecurityValidator:
    """Class to handle comprehensive security validation"""

    @staticmethod
    def validate_input(input_str: str, input_type: str = "general") -> bool:
        """
        Validate input against common security threats
        """
        if not input_str or not isinstance(input_str, str):
            return False

        # Check for SQL injection patterns
        sql_patterns = [
            r"(?i)(union\s+select)",
            r"(?i)(drop\s+table)",
            r"(?i)(insert\s+into)",
            r"(?i)(delete\s+from)",
            r"(?i)(select\s+.+\s+from)",
            r"(?i)(exec\s*\()",
            r"(?i)(';\s*drop\s)",
            r"(?i)(;\s*exec)",
        ]

        for pattern in sql_patterns:
            if re.search(pattern, input_str):
                logger.warning(f"SQL injection attempt detected: {input_str}")
                return False

        # Check for XSS patterns
        xss_patterns = [
            r"<script[^>]*>",
            r"</script>",
            r"javascript:",
            r"vbscript:",
            r"<iframe[^>]*>",
            r"<embed[^>]*>",
            r"<object[^>]*>",
            r"<meta[^>]*>",
        ]

        for pattern in xss_patterns:
            if re.search(pattern, input_str, re.IGNORECASE):
                logger.warning(f"XSS attempt detected: {input_str}")
                return False

        # Validate email format if input_type is email
        if input_type == "email":
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, input_str):
                logger.warning(f"Invalid email format: {input_str}")
                return False

        # Length validation to prevent buffer overflow
        if len(input_str) > 1000:  # Adjust as needed
            logger.warning(f"Input too long (>1000 chars): {input_str[:50]}...")
            return False

        # Validate URL if input_type is url
        if input_type == "url":
            try:
                result = urlparse(input_str)
                if not all([result.scheme, result.netloc]):
                    logger.warning(f"Invalid URL format: {input_str}")
                    return False
            except Exception:
                logger.warning(f"Invalid URL format: {input_str}")
                return False

        return True

    @staticmethod
    def validate_token_security(token: str) -> bool:
        """
        Validate token security aspects
        """
        if not token or not isinstance(token, str):
            return False

        # Check token structure (should be a valid JWT)
        parts = token.split('.')
        if len(parts) != 3:
            logger.warning("Invalid JWT token format")
            return False

        # Verify token signature and validity
        payload = verify_token(token)
        if not payload:
            logger.warning("Invalid or expired token")
            return False

        # Check for required claims
        required_claims = ["exp", "sub", "type"]
        for claim in required_claims:
            if claim not in payload:
                logger.warning(f"Missing required claim '{claim}' in token")
                return False

        return True

    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """
        Sanitize input by removing potentially dangerous characters
        """
        if not input_str or not isinstance(input_str, str):
            return ""

        # Remove potentially dangerous characters
        sanitized = input_str.replace("<", "&lt;").replace(">", "&gt;")
        sanitized = sanitized.replace("\"", "&quot;").replace("'", "&#x27;")
        sanitized = sanitized.replace("(", "&#40;").replace(")", "&#41;")

        # Remove null bytes
        sanitized = sanitized.replace("\0", "")

        return sanitized

    @staticmethod
    def validate_request_security(request: Request) -> bool:
        """
        Validate request security aspects
        """
        # Check for common security headers
        security_headers = [
            "X-Frame-Options",
            "X-Content-Type-Options",
            "X-XSS-Protection",
            "Strict-Transport-Security"
        ]

        # Check for suspicious user agents
        user_agent = request.headers.get("user-agent", "")
        suspicious_agents = [
            "sqlmap",
            "nikto",
            "nessus",
            "acunetix",
            "burp",
            "owasp"
        ]

        for agent in suspicious_agents:
            if agent.lower() in user_agent.lower():
                logger.warning(f"Suspicious user agent detected: {user_agent}")
                return False

        return True

    @staticmethod
    def add_security_headers(response):
        """
        Add security headers to response
        """
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "no-referrer"

        return response