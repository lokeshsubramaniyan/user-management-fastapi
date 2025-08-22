"""
JWT Bearer token authentication module.

This module provides the JWTBearer class for handling JWT token
authentication in FastAPI endpoints.
"""

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.security import verify_token


class JWTBearer(HTTPBearer):
    """
    JWT Bearer token authentication class that extends HTTPBearer.

    This class handles JWT token validation for protected endpoints.
    """

    async def __call__(self, request: Request):
        """
        Validate the JWT token from the request authorization header.

        Args:
            request (Request): The FastAPI request object.

        Returns:
            dict: The decoded token payload if valid.

        Raises:
            HTTPException: If the token is invalid, expired, or missing.
        """
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            payload = verify_token(credentials.credentials)
            if payload:
                return payload
        raise HTTPException(status_code=403, detail="Invalid or expired token")
