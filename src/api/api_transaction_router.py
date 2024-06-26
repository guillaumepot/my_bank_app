"""
API - TRANSACTION ROUTER
"""

"""
LIB
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException

from api_db_connectors import query_for_informations, query_insert_values
from api_vars import generate_uuid


"""
VARS
"""
from api_vars import api_version, available_transactions_types
from api_auth_router import get_current_user

transaction_router = APIRouter()


""" 
TRANSACTION ROUTES
"""

# Get available transaction types
@transaction_router.get(f"/api/{api_version}/available/transaction_types", name="get_available_transaction_types", tags=['transaction'])
def app_get_available_transaction_types(current_user: str = Depends(get_current_user)):
    """
    Retrieves the available transaction types for the current user.

    Parameters:
    - current_user (str): The username of the current user.

    Returns:
    - available_transactions_types (list): A list of available transaction types.

    """
    return available_transactions_types


# Load Transaction Table
@transaction_router.get(f"/api/{api_version}/table/transaction", name="load_transaction_table", tags=['transaction'])
def app_load_transaction_table(current_user: str = Depends(get_current_user)) -> dict:
    """
    Load the existing transactions with all information from the transaction table.

    Parameters:
    - current_user (str): The current user of the application.

    Returns:
    - dict: A dictionary containing the transaction table.

    """
    # Load existing transactions with all information from the transaction table
    results = query_for_informations(request_to_do='get_existing_transactions', additional=None)
    transaction_table = [transaction for transaction in results]
    return {'transaction table': transaction_table}




# Create Transaction
@transaction_router.post(f"/api/{api_version}/create/transaction", name="create_transaction", tags=['transaction'])
def app_create_transaction(transaction_date: str,
                           transaction_type: str,
                           transaction_amount: float,
                           origin_account: str = None,
                           destination_account: str = None,
                           budget_name: str = None,
                           budget_month: str = None,
                           category: str = "Unknown",
                           recipient:str = "Unknown",
                           description: str = "",
                           current_user: str = Depends(get_current_user)) -> dict:
    """

    """

    # Check if balance <= 0
    if transaction_amount <= 0:
        raise HTTPException(status_code=400, detail="Transaction amount must be positive and greater than 0")
    
    # Check if transaction type is valid
    if transaction_type not in available_transactions_types:
        raise HTTPException(status_code=400, detail="Invalid transaction type.")
    
    # Check if account is provided for debit, credit, and transfer transactions
    if transaction_type == "debit" and origin_account is None:
        raise HTTPException(status_code=400, detail="Origin account is required for debit transactions.")
    if transaction_type == "credit" and destination_account is None:
        raise HTTPException(status_code=400, detail="Destination account is required for credit transactions.")
    if transaction_type == "transfer" and (origin_account is None or destination_account is None):
        raise HTTPException(status_code=400, detail="Origin and destination accounts are required for transfer transactions.")

    # If budget None, convert to default budget ID, else get budget ID
    results = query_for_informations(request_to_do='get_existing_budgets', additional=None)

    if budget_name is None:
        # Get default budget ID
        default_budget_info = next((budget for budget in results if budget['name'].strip().lower() == 'default'), None)
        budget_id = default_budget_info.get('id') if default_budget_info else None
        default_budget = True
    else:
        # get the budget ID
        budget_info = next((budget for budget in results if budget['name'].strip().lower() == budget_name.strip().lower() and budget['month'].strip().lower() == budget_month.strip().lower()), None)
        budget_id = budget_info.get('id') if budget_info else None
        default_budget = False

    # Convert date to timestamp
    transaction_date = datetime.strptime(transaction_date, '%Y-%m-%d')

    # Generate transaction id
    transaction_id = generate_uuid()

    # Add the transaction in the table
    values_to_apply = (transaction_id, transaction_date, transaction_type, transaction_amount, origin_account, destination_account, budget_id, category, recipient, description)
    query_insert_values(request_to_do='create_new_transaction', additional=values_to_apply)


    # Apply the transaction to the account
    values_to_apply = (transaction_type, transaction_amount, origin_account, destination_account)   
    query_insert_values(request_to_do='apply_transaction_to_accounts', additional=values_to_apply)

    # Apply the transaction to the budget
    if not default_budget:
        values_to_apply = (transaction_amount, budget_id)
        query_insert_values(request_to_do='apply_transaction_to_budget', additional=values_to_apply)

    return {"message": "Transaction created & applied successfully."}


# Delete Transaction
@transaction_router.delete(f"/api/{api_version}/delete/transaction", name="delete_transaction", tags=['transaction'])
def app_delete_transaction(transaction_id: str, current_user: str = Depends(get_current_user)) -> dict:
    """
    
    """
    query_insert_values(request_to_do='delete_transaction', additional=transaction_id)
    return {"message": f"Transaction with id {transaction_id} deleted successfully."}
