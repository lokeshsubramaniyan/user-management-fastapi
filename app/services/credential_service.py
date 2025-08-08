import logging
from bson.objectid import ObjectId
from fastapi import HTTPException

from app.crud.credential_crud import CredentialCrud
from app.crud.user_crud import UserCrud

logger = logging.getLogger('credential_service')

class CredentialService:
    def __init__(self):
        self.credential_crud = CredentialCrud()
        self.user_crud = UserCrud()

    def create_credential(self, user_id, credential):
        try:
            self.get_user_data(user_id)
            return self.credential_crud.create_credential(user_id, credential)
        except Exception as e:
            logger.error(f'Error occure while creating credential: {e}')
            raise
    
    def get_credential(self, user_id, credential_id):
        try:
            self.get_user_data(user_id)
            credential_id = ObjectId(credential_id)
            credential_data = self.credential_crud.get_credential(user_id, credential_id)
            if not credential_data:
                raise HTTPException(status_code=404, detail=f'Credential not found for credential_id: {credential_id}')
            return self.credential_crud.get_credential(user_id, credential_id)
        except Exception as e:
            logger.error(f'Error occure while getting credential: {e}')
            raise
    
    def get_all_credentials(self, user_id):
        try:
            self.get_user_data(user_id)
            return self.credential_crud.get_all_credentials(user_id)
        except Exception as e:
            logger.error(f'Error occure while getting all credentials: {e}')
            raise
    
    def update_credential(self, user_id, credential_id, credential):
        try:
            self.get_user_data(user_id)
            credential_id = ObjectId(credential_id)
            credential_data = self.credential_crud.get_credential(user_id, credential_id)
            if not credential_data:
                raise HTTPException(status_code=404, detail=f'Credential not found for credential_id: {credential_id}')
            return self.credential_crud.update_credential(user_id, credential_id, credential)
        except Exception as e:
            logger.error(f'Error occure while updating credential: {e}')
            raise
    
    def delete_credential(self, user_id, credential_id):
        try:
            self.get_user_data(user_id)
            credential_id = ObjectId(credential_id)
            credential_data = self.credential_crud.get_credential(user_id, credential_id)
            if not credential_data:
                raise HTTPException(status_code=404, detail=f'Credential not found for credential_id: {credential_id}')
            return self.credential_crud.delete_credential(user_id, credential_id)
        except Exception as e:
            logger.error(f'Error occure while deleting credential: {e}')
            raise

    def get_user_data(self, user_id):
        try:
            user_id = ObjectId(user_id)
            user_data = self.user_crud.get_user(**{'_id': user_id})
            if not user_data:
                raise HTTPException(status_code=404, detail=f'User not found for user_id: {user_id}')
            return user_data
        except Exception as e:
            logger.error(f'Error occure while checking if user is found: {e}')
            raise