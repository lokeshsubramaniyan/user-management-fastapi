"""
User schema module.

This module contains Pydantic models for user data validation,
including User, UpdateUser, and UserLogin models.
"""

from datetime import datetime

from pydantic import BaseModel, field_validator


class User(BaseModel):
    """
    Pydantic model for user data validation and serialization.

    This model defines the structure and validation rules for user data
    including username, password, name, email, and date of birth.
    """

    username: str
    password: str
    name: str
    email_id: str
    date_of_birth: str
    is_deleted: bool = False
    created_at: int = int(datetime.timestamp(datetime.now()))
    updated_at: int = int(datetime.timestamp(datetime.now()))

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        """
        Validate that the password contains at least one capital letter.

        Args:
            value (str): The password to validate.

        Returns:
            str: The validated password.

        Raises:
            ValueError: If the password doesn't contain a capital letter.
        """
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one capital letter")
        return value


class UpdateUser(BaseModel):
    """
    Pydantic model for updating user data.

    This model defines the structure for user update operations,
    excluding the password field for security reasons.
    """

    username: str
    name: str
    email_id: str
    date_of_birth: str
    is_deleted: bool = False
    updated_at: int = int(datetime.timestamp(datetime.now()))


class UserLogin(BaseModel):
    """
    Pydantic model for user login data.

    This model defines the structure for user login requests,
    containing username and password fields.
    """

    username: str
    password: str


class UserResponse(BaseModel):
    """
    Pydantic model for user response data.

    This model defines the structure for user response data,
    containing user data and status code.
    """

    id: str
    username: str
    name: str
    email_id: str
    date_of_birth: str
