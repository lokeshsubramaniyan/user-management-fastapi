from fastapi import APIRouter, Depends, HTTPException
from app.auth.security import authorize
from app.auth.auth_bearer import JWTBearer
from app.services.credential_service import CredentialService
from app.schemas.credentialSchema import Credential

router = APIRouter()
credential_service = CredentialService()

@router.post('/{user_id}/user')
async def create_credential(
    user_id: str, 
    credential: Credential, 
    user: dict = Depends(JWTBearer())
):
    """
    Create a new credential for a specific user.

    Args:
        user_id (str): The ID of the user for whom the credential is being created.
        credential (Credential): The credential data from the request body.
        user (dict): Authenticated user data, injected by JWTBearer.

    Returns:
        str: The ID of the created credential.

    Raises:
        HTTPException(403): If the authenticated user is not authorized.
        HTTPException(500): If any other error occurs during creation.
    """
    try:
        authorize(user_id, user)
        return credential_service.create_credential(user_id, credential)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f'Error creating credential: {e}'
        )

@router.get('/{user_id}/user/{credential_id}')
async def get_credential(
    user_id: str, 
    credential_id: str, 
    user: dict = Depends(JWTBearer())
):
    """
    Retrieve a specific credential by its ID for a user.

    Args:
        user_id (str): The ID of the user who owns the credential.
        credential_id (str): The ID of the credential to retrieve.
        user (dict): Authenticated user data, injected by JWTBearer.

    Returns:
        dict: Credential data if found.

    Raises:
        HTTPException(403): If the authenticated user is not authorized.
        HTTPException(404): If the credential is not found.
        HTTPException(500): If any other error occurs.
    """
    try:
        authorize(user_id, user)
        credential = credential_service.get_credential_by_id(
            user_id, 
            credential_id
        )
        if not credential:
            raise HTTPException(
                status_code=404, 
                detail=f'Credential not found for credential_id: {credential_id}'
            )
        return credential
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f'Error getting credential: {e}'
        )
    
@router.get('/{user_id}/user/{title}/title')
async def get_credential_by_title(
    user_id: str, 
    title: str, 
    user: dict = Depends(JWTBearer())
):
    """
    Retrieve a credential by its title for a user.

    Args:
        user_id (str): The ID of the user who owns the credential.
        title (str): The title of the credential.
        user (dict): Authenticated user data, injected by JWTBearer.

    Returns:
        dict: Credential data if found.

    Raises:
        HTTPException(403): If the authenticated user is not authorized.
        HTTPException(404): If the credential is not found.
        HTTPException(500): If any other error occurs.
    """
    try:
        authorize(user_id, user)
        credential = credential_service.get_credential_by_title(
            user_id, 
            title
        )
        if not credential:
            raise HTTPException(
                status_code=404, 
                detail=f'Credential not found for title: {title}'
            )
        return credential
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f'Error getting credential by title: {e}'
        )

@router.get('/{user_id}/user')
async def get_all_credentials(
    user_id: str, 
    user: dict = Depends(JWTBearer())
):
    """
    Retrieve all credentials for a specific user.

    Args:
        user_id (str): The ID of the user whose credentials are being retrieved.
        user (dict): Authenticated user data, injected by JWTBearer.

    Returns:
        list: A list of all credentials for the user.

    Raises:
        HTTPException(403): If the authenticated user is not authorized.
        HTTPException(500): If any other error occurs.
    """
    try:
        authorize(user_id, user)
        return credential_service.get_all_credentials(user_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f'Error getting all credentials: {e}'
        )

@router.put('/{user_id}/user/{credential_id}/update')
async def update_credential(
    user_id: str, 
    credential_id: str, 
    credential: Credential, 
    user: dict = Depends(JWTBearer())
):
    """
    Update an existing credential for a specific user.

    Args:
        user_id (str): The ID of the user who owns the credential.
        credential_id (str): The ID of the credential to update.
        credential (Credential): The updated credential data.
        user (dict): Authenticated user data, injected by JWTBearer.

    Returns:
        dict: The updated credential data.

    Raises:
        HTTPException(403): If the authenticated user is not authorized.
        HTTPException(404): If the credential is not found.
        HTTPException(500): If any other error occurs.
    """
    try:
        authorize(user_id, user)
        credential_data = credential_service.update_credential(
            user_id, 
            credential_id, 
            credential
        )
        if not credential_data:
            raise HTTPException(
                status_code=404, 
                detail=f'Credential not found for credential_id: {credential_id}'
            )
        return credential_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f'Error updating credential: {e}'
        )

@router.delete('/{user_id}/user/{credential_id}/delete')
async def delete_credential(
    user_id: str, 
    credential_id: str, 
    user: dict = Depends(JWTBearer())
):
    """
    Soft delete a credential for a specific user.

    Args:
        user_id (str): The ID of the user who owns the credential.
        credential_id (str): The ID of the credential to delete.
        user (dict): Authenticated user data, injected by JWTBearer.

    Returns:
        dict: The deletion operation result.

    Raises:
        HTTPException(403): If the authenticated user is not authorized.
        HTTPException(404): If the credential is not found.
        HTTPException(500): If any other error occurs.
    """
    try:
        authorize(user_id, user)
        credential_data = credential_service.delete_credential(
            user_id, 
            credential_id
        )
        if not credential_data:
            raise HTTPException(
                status_code=404, 
                detail=f'Credential not found for credential_id: {credential_id}'
            )
        return credential_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f'Error deleting credential: {e}'
        )
