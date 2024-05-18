#!/bin/bash


# Stop docker compose
docker-compose down

# Remove image
docker image rm personal_bank_app_api:latest