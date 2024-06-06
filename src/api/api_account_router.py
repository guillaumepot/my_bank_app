"""
API - ACCOUNT ROUTER
"""

"""
LIB
"""
import json
from fastapi import APIRouter, Depends, HTTPException

from api_db_connectors import query_for_informations, query_insert_values
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
def app_get_existing_accounts(current_user: str = Depends(get_current_user)) -> dict:
    """
    Retrieve the existing accounts for the current user.

    This function queries the accounts table to fetch the existing accounts for the current user.

    Parameters:
    - current_user (str): The username of the current user.

    Returns:
    - dict: A dictionary containing the available accounts for the current user.

    """
    # Load existing accounts from accounts table
    results = query_for_informations(request_to_do='get_existing_accounts', additional=None)
    existing_accounts = [account[1] for account in results]
    return {'available accounts': existing_accounts}


# Load Account Table
@account_router.get(f"/api/{api_version}/table/account", name="load_account_table", tags=['account'])
def app_load_account_table(current_user: str = Depends(get_current_user)) -> dict:
    """

    """
    # Load existing accounts with all informations from accounts table
    results = query_for_informations(request_to_do='get_existing_accounts', additional=None)

    account_table = [account for account in results]
    return {'account table': account_table}


# Create Account
@account_router.post(f"/api/{api_version}/create/account", name="create_account", tags=['account'])
def app_create_account(account_name: str,
                       account_type: str,
                       account_balance: float,
                       current_user: str = Depends(get_current_user)) -> dict:
    """
    Create a new account for the current user.

    Parameters:
    - account_name (str): The name of the account.
    - account_type (str): The type of the account.
    - account_balance (float): The initial balance of the account.
    - current_user (str, optional): The username of the current user. Defaults to the result of the `get_current_user` function.

    Returns:
    - dict: A dictionary containing a success message and the details of the created account.

    Raises:
    - HTTPException: If the account type is not available, the account balance is negative, or the account name already exists.

    """

    # Check if account type is correct
    if account_type not in available_account_types:
        raise HTTPException(status_code=400, detail="Account type not available")
    
    # Check if balance >0
    if account_balance <0:
        raise HTTPException(status_code=400, detail="Account balance must be positive")

    # Check if account name already exists
    results = query_for_informations(request_to_do='get_existing_accounts', additional = None)
    existing_accounts = [result['name'] for result in results]
    if account_name in existing_accounts:
        raise HTTPException(status_code=400, detail="Account already exists")


    # Generate unique ID for account
    account_id = generate_uuid()

    # Get current user ID
    results = query_for_informations(request_to_do='get_username_informations', additional=current_user)
    current_user_id = results[0][0]

    # Insert new account into accounts table
    account_informations = (account_id, account_name, account_type, account_balance, current_user_id)
    query_insert_values(request_to_do='create_new_account', additional=account_informations)


    return {"message": f"Account {account_name} created successfully." \
                        f"   Type: {account_type}, Balance: {account_balance}" \
                        f"   Owner: {current_user}"}


# Delete Account
@account_router.delete(f"/api/{api_version}/delete/account", name="delete_account", tags=['account'])
def app_delete_account(account_id: str, current_user: str = Depends(get_current_user)) -> dict:
    """
    Deletes an account with the specified account ID.

    Parameters:
    - account_id (str): The ID of the account to be deleted.
    - current_user (str): The current user making the request. Defaults to the result of the `get_current_user` function.

    Returns:
    - dict: A dictionary containing a success message.

    Example:
    >>> app_delete_account("123456")
    {"message": "Account with id 123456 deleted successfully."}
    """

    query_insert_values(request_to_do='delete_account', additional=account_id)
    return {"message": f"Account with id {account_id} deleted successfully."}
