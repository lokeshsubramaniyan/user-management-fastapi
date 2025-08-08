"""
User CRUD operations module.

This module provides the UserCrud class for handling all database
operations related to user management including create, read, update, and delete.
"""

import logging
from datetime import datetime

from app.models.user import user_collection, all_user

logger = logging.getLogger('user_crud')

class UserCrud:
    """
    CRUD operations class for user management in the database.
    
    This class handles all database operations related to users including
    create, read, update, and delete operations.
    """
    
    def __init__(self):
        """
        Initialize the UserCrud class with database collections.
        """
        self.user_collection = user_collection
        self.all_user = all_user

    def get_user(self, **user_details):
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
            user = self.user_collection.find_one(
                {**user_details, 'is_deleted': False}
            )
            logger.info(f'User successfully fetched for user id: {id}')
            return user
        except Exception as e:
            logger.error(f'Error occur while getting user by id: {e}')
            raise

    def create_user(self, user):
        """
        Create a new user in the database.
        
        Args:
            user (dict): The user data to insert into the database.
            
        Returns:
            str: The ID of the newly created user.
            
        Raises:
            Exception: If an error occurs during user creation.
        """
        try:
            response = user_collection.insert_one(user)
            logger.info(f'User created successfully')
            return str(response.inserted_id)
        except Exception as e:
            logger.error(f'Error occure while creating user: {e}')
            raise

    def get_users(self, sort_by, sort_order, filter_params):
        """
        Retrieve all users from the database with sorting and filtering.
        
        Args:
            sort_by (str): The field to sort by.
            sort_order (int): The sort order (1 for ascending, -1 for descending).
            filter_params (dict): The filter parameters to apply.
            
        Returns:
            list: List of user documents matching the criteria.
        """
        users = user_collection.find({'is_deleted': False, **filter_params}).sort(sort_by, sort_order)
        return self.all_user(users)

    def get_user_by_id(self, id):
        """
        Retrieve a user by their ID.
        
        Args:
            id (str): The user's ID.
            
        Returns:
            dict: The user document if found, else None.
        """
        return self.get_user(**{'_id': id})
    
    def update_user_by_id(self, id, user):
        """
        Update a user's information by their ID.
        
        Args:
            id (str): The user's ID.
            user (dict): The updated user data.
            
        Returns:
            UpdateResult: The result of the update operation.
            
        Raises:
            Exception: If an error occurs during the update.
        """
        try:
            user.updated_at = int(datetime.timestamp(datetime.now()))
            response = user_collection.update_one(
                {'_id': id}, 
                {'$set': dict(user)}
            )
            logger.info(f'User successfully updated for user id: {id}')
            return response
        except Exception as e:
            logger.error(f'Error occur while updating user by id: {e}')
            raise
    
    def delete_user_by_id(self, id):
        """
        Mark a user as deleted by setting is_deleted flag to True.
        
        Args:
            id (str): The user's ID.
            
        Returns:
            UpdateResult: The result of the soft delete operation.
            
        Raises:
            Exception: If an error occurs during the deletion.
        """
        try:
            response = self.update_user_by_id(id, {'is_deleted': True})
            logger.info(f'User successfully deleted for user id: {id}')
            return response
        except Exception as e:
            logger.error(f'Error occur while deleting user by id: {e}')
            raise