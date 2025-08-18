from app.models.credential import (
    credential_collection, credential_data, credential_data_update, all_credential,
    credential_data_response
)
from app.core.logger import CustomLogger

logger = CustomLogger('credential_repository')

class CredentialRepository:
    """
    CRUD operations handler for managing user credentials in the database.
    
    This class provides methods to create, read, update, and soft-delete
    credentials associated with a specific user.
    """

    def __init__(self):
        """
        Initialize the CredentialCrud instance with the credential collection
        and data formatting utilities.
        """
        self.credential_collection = credential_collection
        self.all_credential = all_credential
        self.credential_data_response = credential_data_response

    def create_credential(self, user_id, credential):
        """
        Create a new credential for a specific user.

        Args:
            user_id (str): The ID of the user to associate the credential with.
            credential (dict): The credential data to insert.

        Returns:
            str: The ID of the newly created credential document.

        Raises:
            Exception: If an error occurs during the database insertion.
        """
        try:
            response = credential_collection.insert_one(
                credential_data(
                    user_id, 
                    credential
                )
            )
            logger.info(f'Credential created successfully for user_id: {user_id}, credential data: {credential_data(user_id, credential)}, credential id: {response.inserted_id}')
            return str(response.inserted_id)
        except Exception as e:
            logger.error(f'Error occurred while creating credential: {e}')
            raise
    
    def get_credential(self, user_id, credential_query):
        """
        Retrieve a single credential for a user that matches the given query.

        Args:
            user_id (str): The ID of the user whose credential is being retrieved.
            credential_query (dict): Additional query parameters to filter the credential.

        Returns:
            dict: The credential data formatted for response, or None if not found.

        Raises:
            Exception: If an error occurs during the database query.
        """
        try:
            response = credential_collection.find_one(
                {
                    **credential_query,
                    'user_id': user_id,
                    'is_deleted': False
                }
            )
            logger.info(f'Credential fetched successfully for user_id: {user_id}, credential query: {credential_query}')
            return self.credential_data_response(response)
        except Exception as e:
            logger.error(f'Error occurred while getting credential: {e}')
            raise
    
    def get_all_credentials(self, user_id, search_value=None):
        """
        Retrieve all non-deleted credentials for a specific user.

        Args:
            user_id (str): The ID of the user whose credentials are being retrieved.
            search_value (str): The value to search for in the credentials.

        Returns:
            list: A list of all credential data formatted for response.

        Raises:
            Exception: If an error occurs during the database query.
        """
        try:
            search_query = {
                'user_id': user_id, 
                'is_deleted': False
            }
            def get_filter_query(value):
                return {
                    '$or': [
                        {
                            'title': {
                                '$regex': f'^{value}', 
                                '$options': 'i'
                            }
                        },{
                            'username': {
                                '$regex': f'^{value}', 
                                '$options': 'i'
                            }
                        }
                    ]
                }
            if search_value:
                search_query.update(get_filter_query(search_value))
            response = credential_collection.find(search_query)
            logger.info(f'All credentials fetched successfully for user_id: {user_id}, search value: {search_value}, credential count: {response.count()}')
            return self.all_credential(response)
        except Exception as e:
            logger.error(f'Error occurred while getting all credentials: {e}')
            raise
    
    def update_credential(self, user_id, credential_id, credential):
        """
        Update an existing credential for a user.

        Args:
            user_id (str): The ID of the user who owns the credential.
            credential_id (ObjectId): The ID of the credential to update.
            credential (dict): The updated credential data.

        Returns:
            UpdateResult: The result of the update operation.

        Raises:
            Exception: If an error occurs during the update.
        """
        try:
            response = credential_collection.update_one(
                {
                    '_id': credential_id, 
                    'user_id': user_id
                }, {
                    '$set': credential_data_update(credential)
                }
            )
            logger.info(f'Credential updated successfully for user_id: {user_id}, credential id: {credential_id}, credential data: {credential_data_update(credential)}')
            return response
        except Exception as e:
            logger.error(f'Error occurred while updating credential: {e}')
            raise
    
    def delete_credential(self, user_id, credential_id):
        """
        Soft delete a credential by marking it as deleted.

        Args:
            user_id (str): The ID of the user who owns the credential.
            credential_id (ObjectId): The ID of the credential to delete.

        Returns:
            UpdateResult: The result of the update operation.

        Raises:
            Exception: If an error occurs during the deletion process.
        """
        try:
            response = credential_collection.update_one(
                {
                    '_id': credential_id, 
                    'user_id': user_id
                }, {
                    '$set': {'is_deleted': True}
                }
            )
            logger.info(f'Credential deleted successfully for user_id: {user_id}, credential id: {credential_id}')
            return response
        except Exception as e:
            logger.error(f'Error occurred while deleting credential: {e}')
            raise
