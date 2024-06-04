"""
API - MAIN
"""
# Version : 0.2.0
# Current state : Dev
# Author : Guillaume Pot
# Contact : guillaumepot.pro@outlook.com
api_version = "0.2.0"
current_state = "Prod"


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
# Auth
crypt_context_scheme = os.getenv("CRYPT_CONTEXT_SCHEME")
pwd_context = CryptContext(schemes=[crypt_context_scheme], deprecated="auto")

user_file_path = os.getenv("USER_FILE_PATH")
authorized_users = os.getenv("AUTHORIZED_USERS").split(',')

access_token_expiration = int(os.getenv("ACCESS_TOKEN_EXPIRATION"))
algorithm = os.getenv("ALGORITHM")
jwt_secret_key = os.getenv("BANK_APP_API_TOKEN_SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/{api_version}/login")


# Database related variables
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
database = os.getenv('POSTGRES_DB')

engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")


# Value Locks
available_account_types = ("checking", "saving")
available_transactions_types = ("debit", "credit", "transfert")


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

    Parameters:
    - credentials: OAuth2PasswordRequestForm, optional (default: Depends())
        The user's credentials used for authentication.

    Returns:
    - dict: A dictionary containing the access token.

    Raises:
    - HTTPException: If the username or password is incorrect, the user is not authorized, or an error occurs during authentication.

    """
    # Load existing user datas from user_database
    with engine.connect() as conn:

        user_credentials = pd.read_sql("SELECT username, password FROM users", conn)

    username = credentials.username
    password = credentials.password

    if username not in user_credentials['username'].values:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if username not in authorized_users:
        raise HTTPException(status_code=400, detail="User not authorized")
    if not pwd_context.verify(password, user_credentials[user_credentials['username'] == username]["password"].values[0]):
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
                       balance: float,
                       current_user: str = Depends(get_current_user)) -> dict:
    """
    Create a new bank account for the current user.

    Parameters:
    - name (str): The name of the account.
    - type (str): The type of the account (e.g., savings, checking).
    - balance (float): The initial balance of the account.
    - current_user (str, optional): The username of the current user. Defaults to the result of the `get_current_user` function.

    Returns:
    A dictionary containing a success message and the details of the created account.

    Raises:
    - HTTPException: If an account with the same name already exists.

    """
    with engine.connect() as conn:

        # Check if the account name already exists
        account_names = pd.read_sql("SELECT name FROM accounts", conn)
        if name in account_names['name'].values:
            raise HTTPException(status_code=400, detail="Account already exists")
        else:
            # Generate an id for the account
            id = uuid.uuid4()
            owner = pd.read_sql("SELECT id FROM users WHERE username = :username", conn, params={"username": current_user})['id'].values[0]
            history = {}

            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO accounts (id, name, type, balance, owner, history)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (id, name, type, balance, owner, history))

            conn.commit()

    return {"message": f"Account {name} created successfully." \
                        f"Type: {type}, Balance: {balance}" \
                        f"Owner: {current_user}"}


# Delete Account
@app.delete(f"/api/{api_version}/delete/account", name="delete_account", tags=['account'])
def app_delete_account(name: str, current_user: str = Depends(get_current_user)) -> dict:
    """
    
    """
    with engine.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM accounts
            WHERE name = :name
        """, {"name": name})

        conn.commit()

    return {"message": f"Account {name} deleted successfully."}




# Load Account Table
@app.get(f"/api/{api_version}/table/account", name="load_account_table", tags=['account'])
def app_load_account_table(current_user: str = Depends(get_current_user)) -> dict:
    """
    Load the account table from the database and return it as a JSON object.

    Parameters:
    - current_user (str): The username of the current user. Defaults to the result of the `get_current_user` function.

    Returns:
    - dict: A dictionary representing the account table in JSON format.

    """
    with engine.connect() as conn:
        accounts_table = pd.read_sql("SELECT * FROM accounts", conn)
        accounts_table_json = accounts_table.to_json()

    return accounts_table_json



# Get available accounts
@app.get(f"/api/{api_version}/get/account", name="get_available_accounts", tags=['account'])
def app_get_available_accounts(current_user: str = Depends(get_current_user)) -> dict:
    """
    Retrieve the available accounts for the current user.

    Parameters:
    - current_user (str): The username of the current user.

    Returns:
    - dict: A dictionary containing the available accounts as a list under the key 'available accounts'.
    """
    available_accounts = []

    with engine.connect() as conn:
        accounts = pd.read_sql("SELECT name FROM accounts", conn)
        available_accounts = accounts['name'].values

    return {'available accounts': available_accounts}


# Get available account types
@app.get(f"/api/{api_version}/available/account_types", name="get_available_account_types", tags=['account'])
def app_get_available_account_types(current_user:str = Depends(get_current_user)) -> dict:
    """
    Get the available account types for the current user.

    Parameters:
    - current_user (str): The current user's username.

    Returns:
    - available_account_types (list): A list of available account types for the current user.

    """
    return {'available account types': available_account_types}



""" 
Budget routes
"""
# Create Budget
@app.post(f"/api/{api_version}/create/budget", name="create_budget", tags=['budget'])
def app_create_budget(name: str,
                      month: str,
                      amount: float,
                      current_user: str = Depends(get_current_user)) -> dict:
    """
    Create a new budget for the specified month.

    Args:
        name (str): The name of the budget.
        month (str): The month for which the budget is created.
        amount (float): The amount allocated for the budget.
        current_user (str, optional): The current user. Defaults to Depends(get_current_user).

    Returns:
        dict: A dictionary containing a success message with the details of the created budget.

    Raises:
        HTTPException: If a budget with the same name already exists for the specified month.

    """
    with engine.connect() as conn:
        # Check if the budget name already exists for the current month
        budget_names = pd.read_sql("SELECT name FROM budgets WHERE month = :month", conn, params={"month": month})
        if name in budget_names['name'].values:
            raise HTTPException(status_code=400, detail="Budget already exists for this month")
        else:
            # Generate an id for the budget
            id = uuid.uuid4()
            history = {}

            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO accounts (id, name, month, amount, history)
                VALUES (%s, %s, %s, %s, %s)
            """, (id, name, month, amount, history))

            conn.commit()

    return {"message": f"Budget {name} created successfully. Month: {month}, Amount: {amount}"}




# Delete Budget
@app.delete(f"/api/{api_version}/delete/budget", name="delete_budget", tags=['budget'])
def app_delete_budget(name: str, month: str, current_user: str = Depends(get_current_user)) -> dict:
    """
    Deletes a budget from the accounts table.

    Args:
        name (str): The name of the budget.
        month (str): The month of the budget.
        current_user (str, optional): The current user. Defaults to Depends(get_current_user).

    Returns:
        dict: A dictionary containing a success message.
    """
    with engine.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM accounts
            WHERE name = :name AND month = :month
        """, {"name": name, "month": month})

        conn.commit()

    return {"message": f"Budget {name} deleted successfully."}



# Load Budget Table
@app.get(f"/api/{api_version}/table/budget", name="load_budget_table", tags=['budget'])
def app_load_budget_table(current_user: str = Depends(get_current_user)) -> dict:
    """
    Loads the budget table for the current user.

    Parameters:
    - current_user (str): The username of the current user.

    Returns:
    - budget_table (Table): The budget table for the current user.

    """
    with engine.connect() as conn:
        budgets_table = pd.read_sql("SELECT * FROM budgets", conn)
        budgets_table_json = budgets_table.to_json()

    return budgets_table_json



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

    with engine.connect() as conn:
        budgets = pd.read_sql("SELECT name FROM budgets", conn)
        available_budgets = budgets['name'].values

    return {"available budgets": available_budgets}



""" 
Transaction routes
"""
# Create Transaction
@app.post(f"/api/{api_version}/create/transaction", name="create_transaction", tags=['transaction'])
def app_create_transaction(date:str,
                           type:str,
                           amount:float,
                           origin_account:str=None,
                           destination_account:str=None,
                           budget:str=None,
                           budget_month:str=None,
                           category:str="",
                           description:str="",
                           current_user: str = Depends(get_current_user)) -> dict:
    """
    Create a transaction in the bank application.

    Parameters:
    - date (str): The date of the transaction.
    - type (str): The type of the transaction (debit, credit, transfer).
    - amount (float): The amount of the transaction.
    - origin_account (str, optional): The name of the origin account for debit or transfer transactions.
    - destination_account (str, optional): The name of the destination account for credit or transfer transactions.
    - budget (str, optional): The name of the budget for the transaction.
    - budget_month (str, optional): The month of the budget for the transaction.
    - category (str, optional): The category of the transaction.
    - description (str, optional): The description of the transaction.
    - current_user (str, optional): The current user making the transaction.

    Returns:
    - dict: A dictionary containing the message indicating the success of the transaction creation and application.

    Raises:
    - HTTPException: If the transaction type is debit and the origin account is not provided.
    - HTTPException: If the transaction type is credit and the destination account is not provided.
    - HTTPException: If the transaction type is transfer and either the origin or destination account is not provided.
    """

    # Check if the transaction is valid
    if type not in available_transactions_types:
        raise HTTPException(status_code=400, detail="Invalid transaction type.")
    if type == "debit" and origin_account is None:
        raise HTTPException(status_code=400, detail="Origin account is required for debit transactions.")
    if type == "credit" and destination_account is None:
        raise HTTPException(status_code=400, detail="Destination account is required for credit transactions.")
    if type == "transfer" and (origin_account is None or destination_account is None):
        raise HTTPException(status_code=400, detail="Origin and destination accounts are required for transfer transactions.")


    # Create the transaction
    with engine.connect() as conn:
        id = uuid.uuid4()

        if budget == None:
            budget_id = 0
            budget_month = "N/A"
        budget_id = pd.read_sql("SELECT id FROM budgets WHERE name = :budget AND month = :month", conn, params={"budget": budget, "month": budget_month})['id'].values[0]


        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (id, date, type, amount, origin_account, destination_account, budget, category, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (id, date, type, amount, origin_account, destination_account, budget_id, category, description))

        conn.commit()


    # Apply the transaction to the accounts and budgets
    with engine.connect() as conn:
        cursor = conn.cursor()

    if type == "debit":
        cursor.execute("""
            UPDATE accounts
            SET balance = balance - :amount,
                history = history || jsonb_build_object('transaction', :id)
            WHERE name = :origin_account
        """, {"amount": amount, "origin_account": origin_account, "id": str(id)})

    if type == "credit":
        cursor.execute("""
            UPDATE accounts
            SET balance = balance + :amount,
                history = history || jsonb_build_object('transaction', :id)
            WHERE name = :destination_account
        """, {"amount": amount, "destination_account": destination_account, "id": str(id)})

    if type == "transfer":
        cursor.execute("""
            UPDATE accounts
            SET balance = balance - :amount,
                history = history || jsonb_build_object('transaction', :id)
            WHERE name = :origin_account
        """, {"amount": amount, "origin_account": origin_account, "id": str(id)})

        cursor.execute("""
            UPDATE accounts
            SET balance = balance + :amount,
                history = history || jsonb_build_object('transaction', :id)
            WHERE name = :destination_account
        """, {"amount": amount, "destination_account": destination_account, "id": str(id)})

    if budget != None:
        cursor.execute("""
            UPDATE budgets
            SET amount = amount - :amount,
                history = history || jsonb_build_object('transaction', :id)
            WHERE name = :budget AND month = :month
        """, {"amount": amount, "budget": budget, "month": budget_month, "id": str(id)})


    conn.commit()


    return {"message": "Transaction created & applied successfully."}






# Get available transaction types
@app.get(f"/api/{api_version}/available/transaction_types", name="get_available_transaction_types", tags=['transaction'])
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
@app.get(f"/api/{api_version}/table/transaction", name="load_transaction_table", tags=['transaction'])
def app_load_transaction_table(current_user: str = Depends(get_current_user)):
    """
    Load the transaction table from the database and return it as a JSON string.

    Parameters:
    - current_user (str): The username of the current user.

    Returns:
    - str: A JSON string representing the transaction table.

    Raises:
    - None

    Example Usage:
    >>> app_load_transaction_table("john_doe")
    '{"transaction_id": [1, 2, 3], "amount": [100, 200, 300], ...}'
    """
    with engine.connect() as conn:
        transactions_table = pd.read_sql("SELECT * FROM transactions", conn)
        transactions_table_json = transactions_table.to_json()

    return transactions_table_json