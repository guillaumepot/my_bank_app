"""
API - MAIN
"""
# Version : 0.2.0
# Current state : Dev
# Author : Guillaume Pot
# Contact : guillaumepot.pro@outlook.com


"""
LIB
"""
from fastapi import FastAPI


"""
VARS
"""



"""
API declaration
"""

from api_vars import api_version, current_state

app = FastAPI(
    title="Personal bank app",
    description=f"Personal bank app - API {api_version}",
    version=f"{current_state}",
    openapi_tags=[
        {
            'name': 'auth',
            'description': 'Authentication'
        },
        {
            'name': 'home',
            'description': 'Home'
        },
        {
            'name': 'account',
            'description': 'Account'
        },
        {
            'name': 'budget',
            'description': 'Budget'
        },
        {
            'name': 'transaction',
            'description': 'Transaction'
        }   
    ]
)

######################################################################################
"""
API Logger
"""

# LOGGER WIP



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
ROUTERS
"""
from api_auth_router import auth_router
app.include_router(auth_router, tags=["auth"])

from api_account_router import account_router
app.include_router(account_router, tags=["account"])