"""
API - CONFIG VARS
"""


"""
LIBS
"""
import os
import uuid
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer



"""
VARS
"""
# API metadatas
api_version = "0.1.2"
current_state = "Prod"

# UUID Generation
def generate_uuid():
    id = uuid.uuid4()
    id = str(id)
    return id



# Auth
crypt_context_scheme = os.getenv("CRYPT_CONTEXT_SCHEME")
pwd_context = CryptContext(schemes=[crypt_context_scheme], deprecated="auto")

access_token_expiration = int(os.getenv("ACCESS_TOKEN_EXPIRATION"))
algorithm = os.getenv("ALGORITHM")
jwt_secret_key = os.getenv("BANK_APP_API_TOKEN_SECRET_KEY")

authorized_users = os.getenv("AUTHORIZED_USERS").split(',')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/{api_version}/login")


# Value Locks
available_account_types = ("checking", "saving", "investment")
available_transactions_types = ("debit", "credit", "transfert")