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
import os
import jwt
import uuid
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy import create_engine


"""
VARS
"""

######################################################################################
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
