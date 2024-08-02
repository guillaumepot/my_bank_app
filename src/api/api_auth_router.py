"""
API - AUTH ROUTER
"""

"""
LIB
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
import jwt

from api_db_connectors import query_for_informations
from api_main import limiter


"""
VARS
"""
from api_vars import oauth2_scheme, algorithm, jwt_secret_key, access_token_expiration, pwd_context, authorized_users, api_version, auth_limit
auth_router = APIRouter()


"""
AUTH Routes
"""
def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Retrieves the current user based on the provided token.

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


@auth_router.post(f"/api/{api_version}/login", name="login", tags=['auth'])
@limiter.limit(auth_limit) 
async def log_user(request: Request, credentials: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates the user based on the provided credentials and generates an access token.

    Args:
        credentials (OAuth2PasswordRequestForm): The user's login credentials.

    Returns:
        dict: A dictionary containing the access token.

    Raises:
        HTTPException: If the username or password is incorrect, or if the user is not authorized.
    """

    # The username should be in "authorized users" value var
    if credentials.username not in authorized_users:
        raise HTTPException(status_code=400, detail="User not authorized")



    # CREDENTIALS CONTROL

    # Load existing user datas from table
    results = await query_for_informations(request_to_do='get_username_informations', additional = credentials.username)

    # Check if the username is correct
    if credentials.username != results[0]['username']:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


    # The password should be correct
    if not pwd_context.verify(credentials.password, results[0]['password']):
        raise HTTPException(status_code=400, detail="Incorrect username or password")


    # SET TOKEN
    token_expiration = timedelta(minutes=access_token_expiration)
    expire = datetime.now() + token_expiration
    data__to_encode = {"sub": credentials.username, "exp": expire}

    encoded_jwt = jwt.encode(data__to_encode, jwt_secret_key, algorithm=algorithm)

    return {"access_token": encoded_jwt}