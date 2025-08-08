from fastapi import APIRouter, Depends
from app.auth.security import JWTBearer, authorize
from app.services.credential_service import CredentialService
from app.schemas.credentialSchema import Credential

router = APIRouter()
credential_service = CredentialService()

@router.post('{user_id}/user')
async def create_credential(
    user_id: str, 
    credential: Credential, 
    user: dict = Depends(JWTBearer())
):
    authorize(user_id, user)
    return credential_service.create_credential(user_id, credential)

@router.get('{user_id}/user/{credential_id}')
async def get_credential(
    user_id: str, 
    credential_id: str, 
    user: dict = Depends(JWTBearer())
):
    authorize(user_id, user)
    return credential_service.get_credential(user_id, credential_id)

@router.get('{user_id}/user')
async def get_all_credentials(
    user_id: str, 
    user: dict = Depends(JWTBearer())
):
    authorize(user_id, user)
    return credential_service.get_all_credentials(user_id)

@router.put('{user_id}/user/{credential_id}/update')
async def update_credential(
    user_id: str, 
    credential_id: str, 
    credential: Credential, 
    user: dict = Depends(JWTBearer())
):
    authorize(user_id, user)
    return credential_service.update_credential(user_id, credential_id, credential)

@router.delete('{user_id}/user/{credential_id}/delete')
async def delete_credential(
    user_id: str, 
    credential_id: str, 
    user: dict = Depends(JWTBearer())
):
    authorize(user_id, user)
    return credential_service.delete_credential(user_id, credential_id)