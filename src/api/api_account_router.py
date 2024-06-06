"""
API - ACCOUNT ROUTER
"""



"""
LIB
"""
import json
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta

from api_db_connectors import query_pg_db
from api_vars import generate_uuid


"""
VARS
"""
from api_vars import api_version, available_account_types
from api_auth_router import get_current_user

account_router = APIRouter()


""" 
ACCOUNT ROUTES
"""
# Get available account types
@account_router.get(f"/api/{api_version}/available/account_types", name="get_available_account_types", tags=['account'])
def app_get_available_account_types(current_user: str = Depends(get_current_user)) -> dict:
    """
    Retrieves the available account types for the current user.

    Parameters:
    - current_user (str): The current user's username.

    Returns:
    - dict: A dictionary containing the available account types.

    Example:
    >>> app_get_available_account_types('john_doe')
    {'available account types': ['savings', 'checking']}
    """
    return {'available account types': available_account_types}


# Get available accounts
@account_router.get(f"/api/{api_version}/get/account", name="get_available_accounts", tags=['account'])
def app_get_available_accounts(current_user: str = Depends(get_current_user)) -> dict:
    """

    """

    # Load existing accounts from accounts table
    result = query_pg_db(request_to_do='get_existing_accounts', additional = None)
    return {'available accounts': result}


# Create Account
@account_router.post(f"/api/{api_version}/create/account", name="create_account", tags=['account'])
def app_create_account(account_name: str,
                       account_type: str,
                       account_balance: float,
                       current_user: str = Depends(get_current_user)) -> dict:
    """

    """

    # Check if account type is correct
    if account_type not in available_account_types:
        raise HTTPException(status_code=400, detail="Account type not available")
    
    # Check if balance >0
    if account_balance <0:
        raise HTTPException(status_code=400, detail="Account balance must be positive")

    # Check if account name already exists
    result = query_pg_db(request_to_do='get_existing_accounts', additional = None)
    if account_name in result['name']:
        raise HTTPException(status_code=400, detail="Account already exists")


    # Generate unique ID for account
    account_id = generate_uuid()

    # Get current user ID
    result = query_pg_db(request_to_do='get_username_informations', additional=current_user)

    current_user_id = result['id']

    # Generate empty history
    history = json.dumps({})


    # Insert new account into accounts table
    account_informations = (account_id, account_name, account_type, account_balance, current_user_id, history)
    query_pg_db(request_to_do='create_new_account', additional=account_informations, return_attended = 'no')


    return {"message": f"Account {account_name} created successfully." \
                        f"   Type: {account_type}, Balance: {account_balance}" \
                        f"   Owner: {current_user}"}