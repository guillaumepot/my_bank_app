#!/bin/bash


# This script is used to remove a local test.
# This will stop all the containers and services, remove images and remove the postgres datas.


### Step 1 - Stop & remove containers ###

docker compose down

# Remove datas & recreate folder
rm -rf ./storage/postgres_datas/* # /!\ Critical command, be careful with it /!\
mkdir ./storage/postgres_datas

### Step 2 - Remove images ###
docker image rm personal_bank_app_api:test
docker image rm postgres:14