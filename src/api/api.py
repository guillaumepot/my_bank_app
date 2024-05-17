"""
API - MAIN
"""
# Version : 0.1.0
# Current state : Dev
# Author : Guillaume Pot
# Contact : guillaumepot.pro@outlook.com
api_version = "0.1.0"
current_state = "Dev"

"""
LIB
"""
import os
import jwt
import json
from fastapi import FastAPI, Header, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from datetime import datetime, timedelta


from myBankPackage import Account, Budget, Transaction, account_to_table, budget_to_table, available_account_types, available_transactions_types, load_account, load_budget

"""
VARS
"""
# Auth
crypt_context_scheme = os.getenv("CRYPT_CONTEXT_SCHEME")
pwd_context = CryptContext(schemes=[crypt_context_scheme], deprecated="auto")

user_file_path = os.getenv("USER_FILE_PATH")
authorized_users = os.getenv("AUTHORIZED_USERS").split(',')

access_token_expiration = int(os.getenv("ACCESS_TOKEN_EXPIRATION"))
algorithm = os.getenv("ALGORITHM")
jwt_secret_key = os.getenv("BANK_APP_API_TOKEN_SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/{api_version}/login")


# File paths
account_path = os.getenv("ACCOUNT_PATH")
budget_path = os.getenv("BUDGET_PATH")
transaction_path = os.getenv("TRANSACTION_PATH")

"""
API declaration
"""
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
AUTH
"""
def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get the username of the current user based on the provided token.

    Parameters:
    - token (str): The authentication token.

    Returns:
    - str: The username of the current user.

    Raises:
    - HTTPException: If the credentials cannot be validated.

    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    
    try:
        payload = jwt.decode(token, jwt_secret_key, algorithms=[algorithm])
        username = payload.get("sub")
    except Exception as e:
        print(f"An error occurred while decoding the token: {e}")
        raise credentials_exception
    
    return username


@app.post(f"/api/{api_version}/login", name="login", tags=['auth'])
def log_user(credentials: OAuth2PasswordRequestForm = Depends()):
    """
    Logs in a user with the provided credentials and returns an access token.

    Args:
        credentials (OAuth2PasswordRequestForm): The user's login credentials.

    Returns:
        dict: A dictionary containing the access token.

    Raises:
        HTTPException: If the username or password is incorrect, the user is not authorized, or the password verification fails.
    """
    # Load existing user datas from user_database
    with open(user_file_path, "r") as file:
        user_credentials = json.load(file)

    username = credentials.username
    password = credentials.password

    # Check if the user exists and get the current password in the database
    if username not in user_credentials:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if username not in authorized_users:
        raise HTTPException(status_code=400, detail="User not authorized")
    if not pwd_context.verify(password, user_credentials[username]["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token_expiration = timedelta(minutes=access_token_expiration)
    expire = datetime.now() + token_expiration
    data__to_encode = {"sub": credentials.username, "exp": expire}

    encoded_jwt = jwt.encode(data__to_encode, jwt_secret_key, algorithm=algorithm)

    return {"access_token": encoded_jwt}
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
# Create Account
@app.post(f"/api/{api_version}/create/account", name="create_account", tags=['account'])
def app_create_account(name: str,
                       type: str,
                       amount: float,
                       current_user: str = Depends(get_current_user)):
    """
    Create a new bank account for the specified user.

    Parameters:
    name (str): The name of the account holder.
    type (str): The type of the account (e.g., "savings", "checking").
    amount (float): The initial amount to deposit into the account.
    current_user (str, optional): The current user making the request. Defaults to the result of the `get_current_user` function.

    Returns:
    Account: The newly created account.

    """
    account = Account(name, type, amount)
    account.save(account_path)
    return account


# Load Account Table
@app.get(f"/api/{api_version}/table/account", name="load_account_table", tags=['account'])
def app_load_account_table(current_user: str = Depends(get_current_user)):
    """
    Loads the account table for the current user.

    Parameters:
    - current_user (str): The username of the current user.

    Returns:
    - account_table (Table): The account table for the current user.

    """
    account_table = account_to_table(account_path)
    return account_table


# Get available accounts
@app.get(f"/api/{api_version}/get/account", name="get_available_accounts", tags=['account'])
def app_get_available_accounts(current_user: str = Depends(get_current_user)):
    """
    Get the list of available accounts for the current user.

    Parameters:
    - current_user (str): The username of the current user.

    Returns:
    - dict: A dictionary containing the list of available accounts.

    Example:
    >>> app_get_available_accounts('john_doe')
    {'available accounts': ['account1', 'account2', 'account3']}
    """
    available_accounts = []
    for file in os.listdir(account_path):
        available_accounts.append(file)

    return {'available accounts': available_accounts}


# Get available account types
@app.get(f"/api/{api_version}/available/account_types", name="get_available_account_types", tags=['account'])
def app_get_available_account_types(current_user:str = Depends(get_current_user)):
    """
    Get the available account types for the current user.

    Parameters:
    - current_user (str): The current user's username.

    Returns:
    - available_account_types (list): A list of available account types for the current user.

    """
    return available_account_types



""" 
Budget routes
"""
# Create Budget
@app.post(f"/api/{api_version}/create/budget", name="create_budget", tags=['budget'])
def app_create_budget(name: str,
                      month: str,
                      amount: float,
                      current_user: str = Depends(get_current_user)):
    """
    Create a new budget for the current user.

    Parameters:
    - name (str): The name of the budget.
    - month (str): The month for which the budget is created.
    - amount (float): The amount allocated for the budget.
    - current_user (str, optional): The current user. Defaults to the result of the `get_current_user` function.

    Returns:
    - budget: The created budget object.

    """
    budget = Budget(name, month, amount)
    budget.save(budget_path)
    return budget


# Load Budget Table
@app.get(f"/api/{api_version}/table/budget", name="load_budget_table", tags=['budget'])
def app_load_budget_table(current_user: str = Depends(get_current_user)):
    """
    Loads the budget table for the current user.

    Parameters:
    - current_user (str): The username of the current user.

    Returns:
    - budget_table (Table): The budget table for the current user.

    """
    budget_table = budget_to_table(budget_path)
    return budget_table


# Get available budgets
@app.get(f"/api/{api_version}/get/budget", name="get_available_budgets", tags=['budget'])
def app_get_available_budgets(current_user: str = Depends(get_current_user)):
    """
    Get the list of available budgets for the current user.

    Parameters:
    - current_user (str): The username of the current user.

    Returns:
    - dict: A dictionary containing the list of available budgets.

    Example:
    {
        "available budgets": ["budget1", "budget2", "budget3"]
    }
    """
    available_budgets = []
    for file in os.listdir(budget_path):
        available_budgets.append(file)

    return {"available budgets": available_budgets}




""" 
Transaction routes
"""
# Create Transaction
@app.post(f"/api/{api_version}/create/transaction", name="create_transaction", tags=['transaction'])
def app_create_transaction(date:str,
                           type:str,
                           amount:float,
                           origin_account:str,
                           destination_account:str,
                           budget:str,
                           budget_month:str,
                           description:str,
                           current_user: str = Depends(get_current_user)):
    """

    """
    transaction = Transaction(date, type, amount, origin_account, destination_account, budget, budget_month, description)
    transaction.save(transaction_path)
    return transaction


# Apply Transaction
@app.post(f"/api/{api_version}/apply/transaction", name="apply_transaction", tags=['transaction'])
def app_apply_transaction(transaction:Transaction,
                          current_user: str = Depends(get_current_user)):
    """
    
    """
    transaction.apply(account_path, budget_path)
    return {'message':f"Transaction id {transaction.id}, type {transaction.type} applied."}


# Get available transaction types
@app.get(f"/api/{api_version}/available/transaction_types", name="get_available_transaction_types", tags=['transaction'])
def app_get_available_transaction_types(current_user: str = Depends(get_current_user)):
    """
    Get the available transaction types for the current user.

    Parameters:
    - current_user (str): The current user.

    Returns:
    - available_transactions_types: The available transaction types for the current user.
    """
    return available_transactions_types