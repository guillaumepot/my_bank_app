#!/bin/bash


# This script is used to remove a local test.
# This will stop all the containers and services, remove images and remove the postgres datas.


### Step 1 - Stop & remove containers ###

docker compose down
docker container rm container_streamlit -f
docker container rm container_api -f
docker container rm container_postgres -f


# Remove datas & recreate folder
rm -rf ./storage/postgres_datas/* # /!\ Critical command, be careful with it /!\
mkdir ./storage/postgres_datas