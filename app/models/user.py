"""
User model module.

This module provides functions for converting user documents between
database format and API response format.
"""

from app.db_config import db

user_collection = db.get_collection('user_data')

def user_data(user):
    """
    Convert a user document to a dictionary with selected fields.

    Args:
        user (dict): The user document from the database.

    Returns:
        dict: A dictionary containing user id, name, email_id, and date_of_birth.
              Returns an empty dictionary if user is None.
    """
    return {
        'id': str(user['_id']),
        'username': user['username'],
        'name': user['name'],
        'email_id': user['email_id'],
        'date_of_birth': user['date_of_birth']
    } if user else {}
        

def all_user(users):
    """
    Convert a list of user documents to a list of user dictionaries.

    Args:
        users (iterable): An iterable of user documents.

    Returns:
        list: A list of dictionaries, each representing a user.
    """
    return [user_data(user) for user in users]
