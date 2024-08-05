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
async def app_get_available_transaction_types(current_user: str = Depends(get_current_user)):
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
async def app_load_transaction_table(current_user: str = Depends(get_current_user)) -> dict:
    """
    Load the existing transactions with all information from the transaction table.

    Parameters:
    - current_user (str): The current user of the application.

    Returns:
    - dict: A dictionary containing the transaction table.

    """
    # Load existing transactions with all information from the transaction table
    results = await query_for_informations(request_to_do='get_existing_transactions', additional=None)
    transaction_table = [transaction for transaction in results]
    return {'transaction table': transaction_table}


# Display existing categories
@transaction_router.get(f"/api/{api_version}/transaction/categories", name="get_existing_transaction_categories", tags=['transaction'])
async def app_get_existing_transaction_categories(current_user: str = Depends(get_current_user)) -> dict:
    """
    Retrieve the existing transaction categories from the database.

    Returns:
        A dictionary containing the existing categories as a list.
    """
    results = await query_for_informations(request_to_do='get_existing_categories', additional=None)
    print(results) # DEBUG
    existing_categories = [category for category in results]

    return {"existing categories": existing_categories}


# Create Transaction
@transaction_router.post(f"/api/{api_version}/create/transaction", name="create_transaction", tags=['transaction'])
async def app_create_transaction(transaction_date: str,
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
    Create a new transaction and apply it to the accounts and budget.

    Args:
        transaction_date (str): The date of the transaction in the format 'YYYY-MM-DD'.
        transaction_type (str): The type of the transaction.
        transaction_amount (float): The amount of the transaction.
        origin_account (str, optional): The origin account for debit transactions. Defaults to None.
        destination_account (str, optional): The destination account for credit transactions. Defaults to None.
        budget_name (str, optional): The name of the budget. Defaults to None.
        budget_month (str, optional): The month of the budget. Defaults to None.
        category (str, optional): The category of the transaction. Defaults to "Unknown".
        recipient (str, optional): The recipient of the transaction. Defaults to "Unknown".
        description (str, optional): The description of the transaction. Defaults to "".
        current_user (str, optional): The current user. Defaults to Depends(get_current_user).

    Returns:
        dict: A dictionary with a message indicating the success of the transaction creation and application.
    """
    
    # Check if balance <= 0
    if transaction_amount <= 0:
        raise HTTPException(status_code=400, detail="Transaction amount must be positive and greater than 0")

    # Check if transaction type is valid
    if transaction_type not in available_transactions_types:
        raise HTTPException(status_code=400, detail="Invalid transaction type.")
    
    # Check if account is provided for debit, credit, and transfer transactions
    if transaction_type == "debit" and origin_account == "None":
            raise HTTPException(status_code=400, detail="Origin account is required for debit transactions.")
    elif transaction_type == "credit" and destination_account == "None":
        raise HTTPException(status_code=400, detail="Destination account is required for credit transactions.")
    elif transaction_type == "transfer" and (origin_account == "None" or destination_account == "None"):
        raise HTTPException(status_code=400, detail="Origin and destination accounts are required for transfer transactions.")


    #if origin_account =="None" or destination_account == "None":


    # If budget None, convert to default budget ID, else get budget ID
    results = await query_for_informations(request_to_do='get_existing_budgets', additional=None)
    print(results) # DEBUG

    if budget_name is "None":
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
    transaction_id = await generate_uuid()

    # Add the transaction in the table
    values_to_apply = (transaction_id, transaction_date, transaction_type, transaction_amount, origin_account, destination_account, budget_id, category, recipient, description)
    await query_insert_values(request_to_do='create_new_transaction', additional=values_to_apply)


    # Apply the transaction to the account
    values_to_apply = (transaction_type, transaction_amount, origin_account, destination_account)   
    await query_insert_values(request_to_do='apply_transaction_to_accounts', additional=values_to_apply)

    # Apply the transaction to the budget
    if not default_budget:
        values_to_apply = (transaction_amount, budget_id)
        await query_insert_values(request_to_do='apply_transaction_to_budget', additional=values_to_apply)
    
    return {"message": "Transaction created & applied successfully."}


# Delete Transaction
@transaction_router.delete(f"/api/{api_version}/delete/transaction", name="delete_transaction", tags=['transaction'])
async def app_delete_transaction(transaction_id: str, current_user: str = Depends(get_current_user)) -> dict:
    """
    Deletes a transaction from the database and updates the corresponding accounts and budget.

    Args:
        transaction_id (str): The ID of the transaction to be deleted.
        current_user (str, optional): The current user. Defaults to Depends(get_current_user).

    Returns:
        dict: A dictionary containing a success message.

    """
    # Get transaction information
    results = await query_for_informations(request_to_do="get_transaction_by_id", additional=transaction_id)
    
    transaction_info = results[0] if results else None
    transaction_type = transaction_info.get('type')
    transaction_amount = transaction_info.get('amount')
    origin_account = transaction_info.get('origin_account')
    destination_account = transaction_info.get('destination_account')
    budget_id = transaction_info.get('budget')

    # Change the sign of amount
    transaction_amount = -transaction_amount


    # If transaction type is debit, add the amount back to the account
    if transaction_type == 'debit':
        values_to_apply = ('debit', transaction_amount, origin_account, destination_account)
        await query_insert_values(request_to_do='apply_transaction_to_accounts', additional=values_to_apply)

    # If transaction type is credit, remove the amount from the account
    elif transaction_type == 'credit':
        values_to_apply = ('credit', transaction_amount, origin_account, destination_account)
        await query_insert_values(request_to_do='apply_transaction_to_accounts', additional=values_to_apply)

    # If transaction type is transfer, add the amount back to the origin account and remove it from the destination account
    elif transaction_type == 'transfer':
        values_to_apply = ('transfer', transaction_amount, origin_account, destination_account)
        await query_insert_values(request_to_do='apply_transaction_to_accounts', additional=values_to_apply)

    # Apply the transaction to the budget (add the amount back)
    values_to_apply = (transaction_amount, budget_id)
    await query_insert_values(request_to_do='apply_transaction_to_budget', additional=values_to_apply)

    # Delete transaction
    await query_insert_values(request_to_do='delete_transaction', additional=transaction_id)

    
    return {"message": f"Transaction with id {transaction_id} deleted successfully."}
