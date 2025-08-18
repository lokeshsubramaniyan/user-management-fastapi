"""
User service module.

This module provides the UserService class and utility functions for
user management business logic and operations.
"""

from fastapi import HTTPException
from bson.objectid import ObjectId

from app.models.user import user_data
from app.auth.security import hash_password
from app.schemas.userSchema import User
from app.repository.user_repository import UserRepository
from app.core.constants import *
from app.core.logger import CustomLogger

logger = CustomLogger('user_service')
user_repository = UserRepository()

def get_user(**user_details):
    """
    Retrieve a user from the database matching the given details.

    Args:
        **user_details: Arbitrary keyword arguments representing user fields.

    Returns:
        dict: The user document if found, else None.

    Raises:
        Exception: If an error occurs during database query.
    """
    try:
        return user_repository.get_user(**user_details)
    except Exception as e:
        logger.error(f'Error occur while getting user by id: {e}')
        raise

def is_duplicate_username(user: User):
    """
    Check if the username already exists in the database.

    Args:
        user (User): The user object to check.

    Returns:
        User: The user object if no duplicate is found.

    Raises:
        HTTPException: If the username already exists.
    """
    existing_user = user_repository.get_user(**{'username': user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return user

class UserService:
    """
    Service class for user management operations.
    """
    def __init__(self):
        self.user_repository = user_repository

    def create_user(self, user: User):
        """
        Create a new user in the database.

        Args:
            user (User): The user object to create.

        Returns:
            str: The inserted user's ID.

        Raises:
            Exception: If an error occurs during user creation.
        """
        try:
            user.password = hash_password(user.password)
            response = self.user_repository.create_user(dict(user))
            return response
        except Exception as e:
            logger.error(f'Error occure while creating user: {e}')
            raise
    
    def get_users(self, sort_by, sort_order, filter_params):
        """
        Retrieve all non-deleted users from the database.

        Returns:
            list: List of user documents.
        """
        if sort_by not in VALIDATION_FIELDS and sort_by != ID_FIELD:
            raise HTTPException(status_code=400, detail=f'Invalid sort_by field: {sort_by}')
        if not all(key in VALIDATION_FIELDS for key in filter_params.keys()):
            raise HTTPException(status_code=400, detail=f'Invalid filter fields: {filter_params.keys()}')
        sort_order = 1 if 'asc' == sort_order else -1
        if ID_FIELD in filter_params:
            filter_params[MONGO_ID_FIELD] = ObjectId(filter_params[ID_FIELD])
            del filter_params[ID_FIELD]
        users = self.user_repository.get_users(ID_MAP.get(sort_by, sort_by), sort_order, filter_params)
        return users
    
    def get_user_by_id(self, id):
        """
        Retrieve a user by their ID.

        Args:
            id (str): The user's ID.

        Returns:
            dict: The user data if found.

        Raises:
            Exception: If an error occurs during retrieval.
        """
        try:
            user_id = ObjectId(id)
            user = self.user_repository.get_user_by_id(user_id)
            return user_data(user)
        except Exception as e:
            logger.error(f'Error occur while getting user by id: {e}')
            raise

    def update_user_by_id(self, id, user):
        """
        Update a user's information by their ID.

        Args:
            id (str): The user's ID.
            user (User): The updated user object.

        Returns:
            dict or None: The update response or None if user not found.

        Raises:
            Exception: If an error occurs during update.
        """
        try:
            user_id = ObjectId(id)
            user_data = self.user_repository.get_user(**{'_id': user_id})
            if not user_data:
                return user_data
            response = self.user_repository.update_user_by_id(user_id, user)
            return response
        except Exception as e:
            logger.error(f'Error occur while updating user by id: {e}')
            raise

    def delete_user_by_id(self, id: str):
        """
        Mark a user as deleted by their ID.

        Args:
            id (str): The user's ID.

        Returns:
            dict or None: The update response or None if user not found.

        Raises:
            Exception: If an error occurs during deletion.
        """
        try:
            user_id = ObjectId(id)
            user_data = self.user_repository.get_user(**{'_id': user_id})
            if not user_data:
                return user_data
            response = self.user_repository.delete_user_by_id(user_id)
            return response
        except Exception as e:
            logger.error(f'Error occur while deleteing user by id: {e}')
            raise