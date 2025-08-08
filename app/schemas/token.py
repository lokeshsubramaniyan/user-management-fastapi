"""
Token schema module.

This module contains Pydantic models for JWT token responses.
"""

from pydantic import BaseModel

class Token(BaseModel):
    """
    Pydantic model for JWT token response.
    
    This model defines the structure for token responses,
    containing the access token and token type.
    """
    access_token: str
    token_type: str = "bearer"