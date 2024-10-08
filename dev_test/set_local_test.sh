#!/bin/bash

# This script is used to set a local test.
# This will launch all the containers and services needed to run the test.


echo "User credentials for app already generated?"
echo "1. Yes"
echo "2. No"
read -p "Enter your choice: " user_credentials_choice

case $user_credentials_choice in
    1)
        echo "User credentials for app already generated, generation disabled"
        ;;
    2)
        echo "User credentials for app not generated, generation will be enable during Postgres container start"
        ;;
    *)
        echo "Invalid choice. Exiting"
        exit 1
        ;;
esac


if [ $user_credentials_choice -eq 1 ]; then
    export TEST_BANK_APP_TABLE_AND_USER_GENERATION=1
fi



echo "Select containers to run"
echo "1. All containers"
echo "2. Postgres & API container only"
echo "3. Exit"
read -p "Enter your choice: " choice

case $choice in
    1)
        echo "Running all containers"
        ;;
    2)
        echo "Running Postgres & API container only"
        ;;
    3)
        echo "Exiting"
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting"
        exit 1
        ;;
esac



# Set up test venv
echo "Setting up local test environment"
if [ ! -d "test_venv" ]; then
    python3 -m venv test_venv
    source test_venv/bin/activate
    pip install -r ./requirements_test_env.txt

else
    source test_venv/bin/activate
fi
echo "Test venv is ready"

# Set up Docker network
echo "Setting up Docker network"
if [ ! "$(docker network ls | grep bank_app_network)" ]; then
    docker network create bank_app_network
fi


# Start Postgres container
echo "Starting Postgres container"
docker compose -f docker-compose.yaml up -d bank_app_postgres --build
echo "Waiting for Postgres to start"
sleep 20


# Generate tables and test user credentials if not already done
if [ -z "$TEST_BANK_APP_TABLE_AND_USER_GENERATION" ]; then
    echo "Generating tables and test user credentials"
    cd ../utils
    python3 generate_user_credentials.py --user=root --password='root' --db=bank_db --host=localhost --port=5432
    echo "Test user credentials are ready"
fi




# Start API container
echo "Starting API container"
cd ../dev_test
docker compose -f docker-compose.yaml up -d bank_app_api
echo "Waiting for API to start"
sleep 15
echo "API container is up"



# Stop the script if only Postgres and API containers are to be run
if [ $choice -eq 2 ]; then
    echo "Local test environment is ready"
    docker container ls | grep bank_app
    exit 0
fi

# Else run all containers


# Start Streamlit container
echo "Starting Streamlit container"
docker compose -f docker-compose.yaml up -d bank_app_streamlit
echo "Waiting for Streamlit to start"
sleep 15
echo "Streamlit container is up"


echo "Local test environment is ready"
docker container ls | grep bank_app