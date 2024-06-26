# Version : 0.1.0
# Current state : Prod
# Author : Guillaume Pot
# Contact : guillaumepot.pro@outlook.com

# API image
FROM python:3.10

# Define Workdir
WORKDIR /app

# Copy files
COPY ./requirements.txt /app
COPY ./api_main.py /app
COPY ./api_vars.py /app
COPY ./api_db_connectors.py /app
COPY ./api_auth_router.py /app
COPY ./api_account_router.py /app
COPY ./api_budget_router.py /app
COPY ./api_transaction_router.py /app


COPY ./generate_secret_key.py /app
COPY ./generate_secret_key.sh /app


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x ./generate_secret_key.sh


# Port to expose
EXPOSE 8000

# Start uvicorn server
CMD uvicorn api_main:app --host $UVICORN_HOST --port $UVICORN_PORT


# Define the entrypoint
ENTRYPOINT ["./generate_secret_key.sh"]