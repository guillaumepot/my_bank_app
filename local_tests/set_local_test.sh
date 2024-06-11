#!/bin/bash


# This script is used to set a local test.
# This will launch all the containers and services needed to run the test.

# You should have a python env with the required packages installed. (See requirements.txt)



### Step 0 - Add Docker network & Use conda env ###
docker network create bank_app_network

### Step 1 - Start Postgres ###

# Start container
cd ../src/postgres
docker compose up -d

# Generate tables
cd ../../utils
python3 generate_tables.py --user=root --password='root' --db=bank_db --host=localhost --port=5432

# Generate test user credentials
python3 generate_user_credentials.py --user=root --password='root' --db=bank_db --host=localhost --port=5432



### Step 2 - Start API ###

# Build img & Start container
cd ../src/api
docker build -t personal_bank_app_api:latest .
docker compose up -d



### Step 3 - Start Streamlit ###

# Build img & Start container
cd ../src/streamlit
docker build -t personal_bank_app_streamlit:latest .
docker compose up -d