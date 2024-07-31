#!/bin/bash


# This script is used to set a local test.
# This will launch all the containers and services needed to run the test.

# You should have a python venv



### Step 0 - Add Docker network & activate test venv ###
docker network create bank_app_network
source test_venv/bin/activate



### Step 1 - Start Postgres ###

# Start PostGres container
docker compose up -d container_postgres

# Generate tables
cd ../utils
python3 generate_tables.py --user=root --password='root' --db=bank_db --host=localhost --port=5432
# Generate test user credentials
python3 generate_user_credentials.py --user=root --password='root' --db=bank_db --host=localhost --port=5432



### Step 2 - Start API ###

# Build img & Start container
cd ../local_tests
docker compose up -d container_api


### Step 3 - Start Streamlit ###

# Build img & Start container
docker compose up -d container_streamlit