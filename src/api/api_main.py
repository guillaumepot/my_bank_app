"""
API - MAIN
"""

"""
LIB
"""
from fastapi import FastAPI, Request
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware

"""
VARS
"""
# N/C


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


# LIMITER
limiter = Limiter(key_func=get_remote_address)

# Limiter Middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: JSONResponse(
    status_code=429,
    content={"detail": "Rate limit exceeded"}
))

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    return response


######################################################################################
"""
API Logger
"""
# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_logger")

# File handler
# Create a file handler
file_handler = logging.FileHandler('api_logs.log')
file_handler.setLevel(logging.INFO)
# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


# Middleware to sanitize sensitive information
class SanitizeLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Extract client IP
        client_ip = request.client.host

        # Extract request body
        body = await request.body()
        body_str = body.decode("utf-8")

        # Sanitize sensitive information
        if "password" in body_str:
            body_str = body_str.replace("password", "****")

        # Log sanitized request details
        logger.info(f"Request: {request.method} {request.url} from {client_ip} with body: {body_str}")

        # Process request
        response = await call_next(request)

        # Log response status
        logger.info(f"Response status: {response.status_code}\n")
        return response


# Add middleware to the FastAPI application
app.add_middleware(SanitizeLoggingMiddleware)


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

from api_budget_router import budget_router
app.include_router(budget_router, tags=["budget"])

from api_transaction_router import transaction_router
app.include_router(transaction_router, tags=["transaction"])