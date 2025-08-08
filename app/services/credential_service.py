import logging
from bson.objectid import ObjectId
from fastapi import HTTPException

from app.crud.credential_crud import CredentialCrud
from app.crud.user_crud import UserCrud
from app.constants.constants import *

logger = logging.getLogger('credential_service')

class CredentialService:
    """
    Service layer for managing user credentials.

    This class acts as a business logic layer, connecting the CRUD operations 
    for credentials and users. It ensures validation, existence checks, 
    and ID conversions before interacting with the database.
    """

    def __init__(self):
        """
        Initialize the CredentialService with instances of 
        CredentialCrud and UserCrud for data operations.
        """
        self.credential_crud = CredentialCrud()
        self.user_crud = UserCrud()

    def create_credential(self, user_id, credential):
        """
        Create a credential for a given user after validating the user exists.

        Args:
            user_id (str): The ID of the user.
            credential (dict): The credential data to create.

        Returns:
            str: The ID of the created credential.

        Raises:
            HTTPException: If the user does not exist.
            Exception: For any database or processing errors.
        """
        try:
            self.get_user_data(user_id)
            return self.credential_crud.create_credential(user_id, credential)
        except Exception as e:
            logger.error(f'Error occurred while creating credential: {e}')
            raise
    
    def get_credential_by_id(self, user_id, credential_id):
        """
        Retrieve a credential by its ID for a specific user.

        Args:
            user_id (str): The ID of the user.
            credential_id (str): The ID of the credential.

        Returns:
            dict: The credential data, or None if not found.

        Raises:
            HTTPException: If the user does not exist.
            Exception: For any database or processing errors.
        """
        try:
            self.get_user_data(user_id)
            credential_id = ObjectId(credential_id)
            credential_data = self.credential_crud.get_credential(
                user_id, 
                {'_id': credential_id}
            )
            return credential_data
        except Exception as e:
            logger.error(f'Error occurred while getting credential: {e}')
            raise
    
    def get_credential_by_title(self, user_id, title):
        """
        Retrieve a credential by its title for a specific user.

        Args:
            user_id (str): The ID of the user.
            title (str): The title of the credential.

        Returns:
            dict: The credential data, or None if not found.

        Raises:
            HTTPException: If the user does not exist.
            Exception: For any database or processing errors.
        """
        try:
            self.get_user_data(user_id)
            credential_data = self.credential_crud.get_credential(
                user_id, 
                {'title': title}
            )
            return credential_data
        except Exception as e:
            logger.error(f'Error occurred while getting credential by title: {e}')
            raise
    
    def get_all_credentials(self, user_id):
        """
        Retrieve all credentials for a specific user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            list: A list of all credentials for the user.

        Raises:
            HTTPException: If the user does not exist.
            Exception: For any database or processing errors.
        """
        try:
            self.get_user_data(user_id)
            return self.credential_crud.get_all_credentials(user_id)
        except Exception as e:
            logger.error(f'Error occurred while getting all credentials: {e}')
            raise
    
    def update_credential(self, user_id, credential_id, credential):
        """
        Update a credential for a specific user.

        Args:
            user_id (str): The ID of the user.
            credential_id (str): The ID of the credential to update.
            credential (dict): The updated credential data.

        Returns:
            UpdateResult or None: The update operation result, or None if the credential does not exist.

        Raises:
            HTTPException: If the user does not exist.
            Exception: For any database or processing errors.
        """
        try:
            self.get_user_data(user_id)
            credential_id = ObjectId(credential_id)
            credential_data = self.credential_crud.get_credential(
                user_id, 
                {'_id': credential_id}
            )
            if not credential_data:
                return None
            return self.credential_crud.update_credential(
                user_id, 
                credential_id, 
                credential
            )
        except Exception as e:
            logger.error(f'Error occurred while updating credential: {e}')
            raise
    
    def delete_credential(self, user_id, credential_id):
        """
        Soft delete a credential for a specific user.

        Args:
            user_id (str): The ID of the user.
            credential_id (str): The ID of the credential to delete.

        Returns:
            UpdateResult or None: The deletion operation result, or None if the credential does not exist.

        Raises:
            HTTPException: If the user does not exist.
            Exception: For any database or processing errors.
        """
        try:
            self.get_user_data(user_id)
            credential_id = ObjectId(credential_id)
            credential_data = self.credential_crud.get_credential(
                user_id, 
                {'_id': credential_id}
            )
            if not credential_data:
                return None
            return self.credential_crud.delete_credential(
                user_id, 
                credential_id
            )
        except Exception as e:
            logger.error(f'Error occurred while deleting credential: {e}')
            raise

    def get_user_data(self, user_id):
        """
        Validate and retrieve user data by ID.

        Args:
            user_id (str): The ID of the user to retrieve.

        Returns:
            dict: The user data.

        Raises:
            HTTPException: If the user is not found.
            Exception: For any database or processing errors.
        """
        try:
            user_id = ObjectId(user_id)
            user_data = self.user_crud.get_user(**{'_id': user_id})
            if not user_data:
                raise HTTPException(
                    status_code=404, 
                    detail=f'User not found for user_id: {user_id}'
                )
            return user_data
        except Exception as e:
            logger.error(f'Error occurred while checking if user is found: {e}')
            raise
