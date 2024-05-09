"""
API - MAIN
"""

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


from myBankPackage import Account

"""
VARS
"""
api_version = "0.1.0" # Update changelogs and version in the README.md file
current_state = "Dev" # Update changelogs and version in the README.md file


# Auth
crypt_context_scheme = os.getenv("CRYPT_CONTEXT_SCHEME")
pwd_context = CryptContext(schemes=[crypt_context_scheme], deprecated="auto")

user_file_path = os.getenv("USER_FILE_PATH")
authorized_users = os.getenv("AUTHORIZED_USERS").split(',')

access_token_expiration = os.getenv("ACCESS_TOKEN_EXPIRATION")
algorithm = os.getenv("ALGORITHM")
jwt_secret_key = os.getenv("BANK_APP_API_TOKEN_SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/{api_version}/login")


# File paths
account_path = os.getenv("ACCOUNT_PATH")

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
def get_current_user(token: str = Depends(oauth2_scheme)):

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

######################################################################################
"""
AUTH
"""
@app.post(f"/api/{api_version}/login", name="login", tags=['auth'])
def log_user(credentials: OAuth2PasswordRequestForm = Depends()):
    """
    
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

    access_token_expiration = timedelta(minutes=access_token_expiration)
    expire = datetime.utcnow() + access_token_expiration
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
@app.post(f"/api/{api_version}/create/account", name="account", tags=['create', 'account'])
def app_create_account(name:str,
                       type:str,
                       amount:float,
                       current_user: str = Depends(get_current_user)) -> None:
    """

    """
    account = Account(name, type, amount)
    account.save(account_path)
    print(f"Account created: {account["name"]} - {account["type"]} - {account["amount"]}")
    return {"account": account.__dict__}


