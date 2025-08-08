
"""
Utility functions module.

This module contains utility functions used throughout the application
for parameter processing and other common operations.
"""

from app.constants.constants import *

def get_params(params):
    """
    Extract and process query parameters for sorting and filtering.
    
    This function extracts sort_by and sort_type parameters from the query params
    and returns them along with the remaining filter parameters.
    
    Args:
        params (dict): Dictionary containing query parameters.
        
    Returns:
        tuple: A tuple containing (sort_by, sort_type, filter_params) where:
            - sort_by (str): The field to sort by (defaults to 'id')
            - sort_type (str): The sort order (defaults to 'asc')
            - filter_params (dict): Remaining parameters for filtering
    """
    sort_by = params.get(SORT_BY_FIELD, ID_FIELD)
    sort_type = params.get(SORT_TYPE_FIELD, SORT_TYPE_ASC)
    params.pop(SORT_BY_FIELD, None)
    params.pop(SORT_TYPE_FIELD, None)
    return sort_by, sort_type, params