"""
Security module for authentication and authorization.

This module provides functions for password hashing, JWT token creation
and verification, and access control functionality.
"""

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import HTTPException
from app.core.constants import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    """
    Hash a plain password using bcrypt.

    Args:
        password (str): The plain password.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): The plain password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    if not plain_password or not hashed_password:
        return False
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a JWT access token.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (timedelta, optional): The expiration time for the token.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    """
    Verify and decode a JWT token.

    Args:
        token (str): The JWT token to verify.

    Returns:
        dict or None: The decoded payload if valid, None otherwise.
    """
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    
def allow_access(id, current_user):
    """
    Check if the current user is allowed to access the resource.

    Args:
        id (str): The resource/user id.
        current_user (dict): The current authenticated user.

    Returns:
        bool: True if access is allowed, False otherwise.
    """
    if id != current_user.get('id', ''):
        return False
    return True

def authorize(id, current_user):
    """
    Authorize the current user for the given user ID.

    Args:
        id (str): The user ID to authorize.
        current_user: The current user object.

    Returns:
        current_user: The current user if authorized.

    Raises:
        HTTPException: If the user is not authorized.
    """
    if not allow_access(id, current_user):
        raise HTTPException(status_code=401, detail='Unauthorised action')
    return current_user