"""
Constants module for the user management application.

This module contains all the constant values used throughout the application
including field mappings, sort types, search types, and validation fields.
"""

from app.schemas.userSchema import User
import os
from dotenv import load_dotenv
load_dotenv()

ID_MAP = {
    'id': '_id',
}
ID_FIELD = 'id'
MONGO_ID_FIELD = '_id'
SORT_TYPE_ASC = 'asc'
SORT_TYPE_DESC = 'desc'
SORT_BY_FIELD = 'sort_by'
SORT_TYPE_FIELD = 'sort_type'
SEARCH_BY_FIELD = 'search_by'
SEARCH_VALUE_FIELD = 'search_value'
VALIDATION_FIELDS = User.__dict__['__annotations__'].keys()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')



SEARCH_TYPE_FIELD = 'search_type'
SEARCH_TYPE_EXACT = 'exact'
SEARCH_TYPE_PARTIAL = 'partial'
SEARCH_TYPE_REGEX = 'regex'
SEARCH_TYPE_WILDCARD = 'wildcard'
SEARCH_TYPE_FUZZY = 'fuzzy'
SEARCH_TYPE_PHONETIC = 'phonetic'