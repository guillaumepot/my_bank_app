#####
# TEMPORARY VARIABLES
#####
#
#
#
algorithm="HS256"
access_token_expiration = 60
crypt_context_scheme="argon2"
authorized_users ="root"
jwt_secret_key="root"
authorized_users="root"
#
#
#
#####
# END OF TEMPORARY VARIABLES
#####

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
api_version = "0.2.0"
current_state = "Dev"

# UUID Generation
def generate_uuid():
    id = uuid.uuid4()
    id = str(id)
    return id



# Auth
#crypt_context_scheme = os.getenv("CRYPT_CONTEXT_SCHEME")
pwd_context = CryptContext(schemes=[crypt_context_scheme], deprecated="auto")

#authorized_users = os.getenv("AUTHORIZED_USERS").split(',')

#access_token_expiration = int(os.getenv("ACCESS_TOKEN_EXPIRATION"))
#algorithm = os.getenv("ALGORITHM")
#jwt_secret_key = os.getenv("BANK_APP_API_TOKEN_SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/{api_version}/login")


# Value Locks
available_account_types = ("checking", "saving")
available_transactions_types = ("debit", "credit", "transfert")