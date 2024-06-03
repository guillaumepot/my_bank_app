#!/bin/bash

# Create network
docker network create bank_app_network


# Copy table generator
cp ../../utils/generate_tables.py .

# Build image
docker build -t personal_bank_app_postgres:latest -f ./Dockerfile.postgres .


# Start container
docker compose -f docker-compose.yaml up -d

# Remove copied files
rm generate_tables.py