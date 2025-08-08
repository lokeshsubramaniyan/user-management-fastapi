"""
User API router module.

This module contains all the user-related API endpoints including
CRUD operations, authentication, and user management functionality.
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from bson.objectid import ObjectId
from datetime import datetime
import logging
import traceback

from app.models.user import user_data, all_user, user_collection
from app.schemas.token import Token
from app.schemas.userSchema import User, UpdateUser, UserLogin, UserResponse
from app.services.user_service import (
    UserService, is_duplicate_username, get_user, authorize
)
from app.auth.security import (
    verify_password, create_access_token, verify_token
)
from app.auth.auth_bearer import JWTBearer
from app.constants.constants import *
from app.utilities.util import get_params

logger = logging.getLogger('users')
router = APIRouter()
user_service = UserService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str):
    """
    Retrieve the current user based on the provided OAuth2 token.

    Args:
        token (str): The OAuth2 token.

    Returns:
        dict: The user data if token is valid.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    user_data = verify_token(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user_data

@router.post('')
async def create_user(user: User = Depends(is_duplicate_username)) -> dict:
    """
    Create a new user.

    Args:
        user (User): The user object, validated for duplicate username.

    Returns:
        dict: Status code and created user data.

    Raises:
        HTTPException: If an error occurs during user creation.
    """
    try:
        response = user_service.create_user(user)
        logger.info(f'User created successfully')
        return {'status_code': 200, 'data': response}
    except Exception as e:
        logger.error(f'Unknown error occure while creating user: {e}')
        raise HTTPException(
            status_code=500, 
            detail=f'Exception occur while creating user: {e}'
        )

@router.get('', dependencies=[Depends(JWTBearer())])
async def get_all_user(
    request: Request,
) -> list[dict]:
    """
    Retrieve all users.

    Args:
        current_user (dict): The current authenticated user.

    Returns:
        list[dict]: List of user data.
    """
    sort_by, sort_type, filter_params = get_params(dict(request.query_params))
    return user_service.get_users(sort_by, sort_type, filter_params)

@router.get(
    path='/{id}/user',
    response_model=UserResponse
)
async def get_user_by_id(
    id: str, 
    current_user: dict = Depends(JWTBearer())
) -> dict:
    """
    Retrieve a user by their ID.

    Args:
        id (str): The user's ID.
        current_user (dict): The current authenticated user.

    Returns:
        dict: Status code and user data.

    Raises:
        HTTPException: If user is not found or an error occurs.
    """
    try:
        authorize(id, current_user)
        user = user_service.get_user_by_id(id)
        if not user:
            logger.error(f'User not found for user id: {id}')
            raise HTTPException(
                status_code=404, 
                detail=f'User not found for id: {id}'
            )
        logger.info(f'User successfully fetched for user id: {id}')
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Unknown error occure while fetching user: {e}')
        raise HTTPException(
            status_code=500, 
            detail=f'Exception occur while updating user: {e}'
        )

@router.put('/{id}/update')
async def update_user_by_id(
    id: str, 
    user: UpdateUser,
    current_user: dict = Depends(JWTBearer())
):
    """
    Update a user by their ID.

    Args:
        id (str): The user's ID.
        user (User): The updated user object.
        current_user (dict): The current authenticated user.

    Returns:
        dict: Status code and update message.

    Raises:
        HTTPException: If user is not found or an error occurs.
    """
    try:
        authorize(id, current_user)
        user_data = user_service.update_user_by_id(id, user)
        if not user_data:
            logger.error(f'User not found for user id: {id}')
            raise HTTPException(
                status_code=404, 
                detail=f'User not found for id: {id}'
            )
        return {'status_code': 200, 'message': 'User updated successfully'}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Unknown error occure while updating user: {traceback.format_exc()}')
        raise HTTPException(
            status_code=500, 
                detail=f'Exception occur while updating user: {e}'
            )

@router.delete('/{id}/delete')
async def delete_user_by_id(
    id: str,
    current_user: dict = Depends(JWTBearer())
):
    """
    Delete a user by their ID.

    Args:
        id (str): The user's ID.
        current_user (dict): The current authenticated user.

    Returns:
        dict: Status code and deletion message.

    Raises:
        HTTPException: If user is not found or an error occurs.
    """
    try:
        authorize(id, current_user)
        user_data = user_service.delete_user_by_id(id)
        if not user_data:
            logger.error(f'User not found for user id: {id}')
            raise HTTPException(
                status_code=404, 
                detail=f'User not found for id: {id}'
            )
        return {'status_code': 200, 'message': 'User deleted successfully'}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Unknown error occure while daleting user: {e}')
        raise HTTPException(
            status_code=500, 
            detail=f'Exception occur while updating user: {e}'
        )

@router.post('/login', response_model=Token)
async def login(form_data: UserLogin):
    """
    Authenticate a user and return an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The login form data.

    Returns:
        dict: Access token and token type.

    Raises:
        HTTPException: If credentials are invalid or password is incorrect.
    """
    user = get_user(**{'username': form_data.username})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(form_data.password, user.get('password')):
        raise HTTPException(status_code=401, detail="Incorrect password")
    token = create_access_token(user_data(user))
    return {"access_token": token, "token_type": "bearer"}

@router.get('/me')
async def me(user: dict = Depends(JWTBearer())):
    """
    Get the current authenticated user's information.
    
    Args:
        user (dict): The current authenticated user data from JWT token.
        
    Returns:
        dict: The current user's information.
    """
    return user

