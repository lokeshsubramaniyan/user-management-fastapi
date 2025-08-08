import logging

from app.models.credential import (
    credential_collection, credential_data, credential_data_update
)

logger = logging.getLogger('credential_crud')

class CredentialCrud:
    def __init__(self):
        self.credential_collection = credential_collection

    def create_credential(self, user_id, credential):
        try:
            response = credential_collection.insert_one(
                credential_data(
                    user_id, 
                    credential
                )
            )
            logger.info(f'Credential created successfully')
            return str(response.inserted_id)
        except Exception as e:
            logger.error(f'Error occure while creating credential: {e}')
            raise
    
    def get_credential(self, user_id, credential_id):
        try:
            response = credential_collection.find_one(
                {
                    '_id': credential_id, 
                    'user_id': user_id,
                    'is_deleted': False
                }
            )
            return response
        except Exception as e:
            logger.error(f'Error occure while getting credential: {e}')
            raise
    
    def get_all_credentials(self, user_id):
        try:
            response = credential_collection.find(
                {
                    'user_id': user_id, 
                    'is_deleted': False
                }
            )
            return response
        except Exception as e:
            logger.error(f'Error occure while getting all credentials: {e}')
            raise
    
    def update_credential(self, user_id, credential_id, credential):
        try:
            response = credential_collection.update_one(
                {
                    '_id': credential_id, 
                    'user_id': user_id
                }, {
                    '$set': credential_data_update(credential)
                }
            )
            return response
        except Exception as e:
            logger.error(f'Error occure while updating credential: {e}')
            raise
    
    def delete_credential(self, user_id, credential_id):
        try:
            response = credential_collection.update_one(
                {
                    '_id': credential_id, 
                    'user_id': user_id
                }, {
                    '$set': {'is_deleted': True}
                }
            )
            return response
        except Exception as e:
            logger.error(f'Error occure while deleting credential: {e}')
            raise
