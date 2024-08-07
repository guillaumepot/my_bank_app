"""
API - ACCOUNT ROUTER
"""

"""
LIB
"""
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
async def app_get_existing_accounts(current_user: str = Depends(get_current_user)) -> dict:
    """
    Retrieve the existing accounts for the current user.

    Parameters:
    - current_user (str): The current user.

    Returns:
    - dict: A dictionary containing the available accounts.

    Raises:
    - HTTPException: If there is an error retrieving the accounts.
    """
    try:
        # Load existing accounts from accounts table
        results = await query_for_informations(request_to_do='get_existing_accounts', additional=None)
        existing_account_names = [account['name'] for account in results]
        return {'available accounts': existing_account_names}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Load Account Table
@account_router.get(f"/api/{api_version}/table/account", name="load_account_table", tags=['account'])
async def app_load_account_table(current_user: str = Depends(get_current_user)) -> dict:
    """
    Load the existing accounts with all information from the accounts table.

    Parameters:
    - current_user (str): The current user.

    Returns:
    - dict: A dictionary containing the account table.

    Raises:
    - HTTPException: If there is an error while loading the account table.
    """
    try:
        # Load existing accounts with all information from the accounts table
        results = await query_for_informations(request_to_do='get_existing_accounts', additional=None)
        account_table = [account for account in results]
        return {'account table': account_table}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create Account
@account_router.post(f"/api/{api_version}/create/account", name="create_account", tags=['account'])
async def app_create_account(account_name: str,
                       account_type: str,
                       account_balance: float,
                       current_user: str = Depends(get_current_user)) -> dict:
    """
    Create a new account for the current user.

    Args:
        account_name (str): The name of the account.
        account_type (str): The type of the account.
        account_balance (float): The initial balance of the account.
        current_user (str, optional): The username of the current user. Defaults to the result of the `get_current_user` function.

    Returns:
        dict: A dictionary containing the details of the created account.

    Raises:
        HTTPException: If the account type is not available, the account balance is negative, or the account name already exists.

    """

    # Check if account type is correct
    if account_type not in available_account_types:
        raise HTTPException(status_code=400, detail="Account type not available")
    
    # Check if balance >0
    if account_balance <0:
        raise HTTPException(status_code=400, detail="Account balance must be positive")


    try:
        # Check if account name already exists
        results = await query_for_informations(request_to_do='get_existing_accounts', additional = None)
        existing_accounts = [result['name'] for result in results]

        if account_name in existing_accounts:
            raise HTTPException(status_code=400, detail="Account already exists")
    

        # Generate unique ID for account
        account_id = await generate_uuid()

        # Get current user ID
        results = await query_for_informations(request_to_do='get_username_informations', additional=current_user)
        current_user_id = results[0]["id"]

        # Insert new account into accounts table
        account_informations = (account_id, account_name, account_type, account_balance, current_user_id)
        await query_insert_values(request_to_do='create_new_account', additional=account_informations)


        return {"message": f"Account {account_name} created successfully." \
                            f"   Type: {account_type}, Balance: {account_balance}" \
                            f"   Owner: {current_user}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# Delete Account
@account_router.delete(f"/api/{api_version}/delete/account", name="delete_account", tags=['account'])
async def app_delete_account(account_id: str, current_user: str = Depends(get_current_user)) -> dict:
    """
    Delete an account with the specified account ID.

    Parameters:
    - account_id (str): The ID of the account to be deleted.
    - current_user (str, optional): The current user. Defaults to the result of the `get_current_user` function.

    Returns:
    - dict: A dictionary containing a success message.

    Raises:
    - HTTPException: If an error occurs during the deletion process.

    """
    try:
        await query_insert_values(request_to_do='delete_account', additional=account_id)
        return {"message": f"Account with id {account_id} deleted successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
