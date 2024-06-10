#!/bin/bash


# This script is used to remove a local test.
# This will stop all the containers and services, remove images and remove the postgres datas.


### Step 1 - Stop Streamlit ###

# Stop container & remove image
cd ../src/streamlit
docker compose down
docker container rm container_streamlit -f
docker image rm personal_bank_app_streamlit:latest -f



### Step 2 - Stop API ###

# Stop container & remove image
cd ../src/api
docker compose down
docker container rm container_api -f
docker image rm personal_bank_app_api:latest -f



### Step 3 - Stop Postgres ###

# Stop container & remove image
cd ../src/postgres
docker compose down
docker container rm container_postgres -f
docker image rm postgres:13 -f

# Remove datas
cd ../../storage/postgres
rm -rf * # /!\ Critical command, be careful with it /!\