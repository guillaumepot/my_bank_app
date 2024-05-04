"""
API - MAIN
"""

"""
LIB
"""
from fastapi import FastAPI, Header, Request

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
@app.get(f"/api/{api_version}/account", name="account", tags=['account'])
async def get_account(account_name: str) -> None:
    """

    """

