"""
API - MAIN
"""

"""
LIB
"""
from fastapi import FastAPI, Header, Request
from functions import load_specific_account


"""
VARS
"""
api_version = "v0.1" # Update changelogs and version in the README.md file
current_state = "Dev" # Update changelogs and version in the README.md file

"""
API declaration
"""
app = FastAPI(
    title="Personal bank app",
    description=f"Personal bank app - API {api_version}",
    version=f"{current_state}",
    openapi_tags=[
        {
            'name': 'home',
            'description': 'Home'
        },
        {
            'name': 'account',
            'description': 'Account'
        },
        {
            'name': 'create',
            'description': 'Creation functions (accounts, budgets, transactions, ...)'
        },
        {
            'name': 'budget',
            'description': 'Budget'
        }
    ]
)


###############################################################

"""
API Logger
"""

# LOGGER WIP



######################################################################################
"""
FUNCTIONS
"""
import myBankPackage as mbp











######################################################################################
"""
ROUTES
"""

"""
home routes
"""
# status route
@app.get(f"/api/{api_version}/status", name="status", tags=['home'])
async def get_status() -> dict:
    """
    Get the status of the API.

    Returns:
        dict: A dictionary containing the status, version, and current state of the API.
    """
    return {"status": "Working", "version": api_version, "current_state": current_state}



""" 
Account routes
"""
@app.post(f"/api/{api_version}/create/account", name="account", tags=['create', 'account'])
def app_create_account() -> None:
    """

    """

