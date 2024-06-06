"""
API - BUDGET ROUTER
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
from api_vars import api_version
from api_auth_router import get_current_user

budget_router = APIRouter()


""" 
BUDGET ROUTES
"""
# Get available budgets
@budget_router.get(f"/api/{api_version}/get/budget", name="get_available_budgets", tags=['budget'])
def app_get_available_budgets(current_user: str = Depends(get_current_user)) -> dict:
    """
    Retrieve the available budgets for the current user.

    Parameters:
    - current_user (str): The username of the current user.

    Returns:
    - dict: A dictionary containing the available budgets for the current user.

    """
    # Load existing budgets from budgets table
    results = query_for_informations(request_to_do='get_existing_budgets', additional=None)
    existing_budgets = [budget[1] for budget in results if budget[1] != 'default']   # Remove default budget from the list
    return {'available budgets': existing_budgets}


# Load Budget Table
@budget_router.get(f"/api/{api_version}/table/budget", name="load_budget_table", tags=['budget'])
def app_load_budget_table(current_user: str = Depends(get_current_user)) -> dict:
    """
    Load the existing budgets with all information from the budget table.

    Parameters:
    - current_user (str): The username of the current user.

    Returns:
    - dict: A dictionary containing the budget table.

    """
    # Load existing budgets with all information from the budget table
    results = query_for_informations(request_to_do='get_existing_budgets', additional=None)
    budget_table = [budget for budget in results if budget[1] != 'default'] # Remove default budget from the list
    return {'budget table': budget_table}


# Create Budget
@budget_router.post(f"/api/{api_version}/create/budget", name="create_budget", tags=['budget'])
def app_create_budget(budget_name: str,
                       budget_month: str,
                       budget_amount: float,
                       current_user: str = Depends(get_current_user)) -> dict:
    """
    Create a new budget for the current user.

    Parameters:
    - budget_name (str): The name of the budget.
    - budget_month (str): The month for which the budget is created.
    - budget_amount (float): The amount allocated for the budget.
    - current_user (str, optional): The current user. Defaults to the result of the `get_current_user` function.

    Returns:
    - dict: A dictionary containing a success message with the details of the created budget.

    Raises:
    - HTTPException: If the budget amount is negative or if a budget with the same name and month already exists.

    """
    # Check if balance <0
    if budget_amount <0:
        raise HTTPException(status_code=400, detail="Budget balance must be positive")

    # Check if budget name already exists (at a precise month)
    results = query_for_informations(request_to_do='get_existing_budgets', additional = None)
    existing_budgets = [result[1:3] for result in results] # Get budget name & month
    if (budget_name, budget_month) in existing_budgets:
        raise HTTPException(status_code=400, detail="Budget already exists")


    # Generate unique ID for budget
    budget_id = generate_uuid()

    # Generate empty history
    history = json.dumps({})


    # Insert new budget into budget table
    budget_informations = (budget_id, budget_name, budget_month, budget_amount, history)
    query_insert_values(request_to_do='create_new_budget', additional=budget_informations)

    return {"message": f"Budget {budget_name} created successfully." \
                        f"   Month: {budget_month}, Balance: {budget_amount}"}


# Delete Budget
@budget_router.delete(f"/api/{api_version}/delete/budget", name="delete_budget", tags=['budget'])
def app_delete_budget(budget_id: str, current_user: str = Depends(get_current_user)) -> dict:
    """
    Delete a budget with the given budget_id.

    Parameters:
    - budget_id (str): The ID of the budget to be deleted.
    - current_user (str): The current user making the request. Defaults to the result of the `get_current_user` function.

    Returns:
    - dict: A dictionary containing a message indicating the success of the deletion.

    """
    query_insert_values(request_to_do='delete_budget', additional=budget_id)
    return {"message": f"Budget with id {budget_id} deleted successfully."}
