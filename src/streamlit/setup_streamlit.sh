#!/bin/bash

# Create network
docker network create bank_app_network

# Build image
docker build -t postgres_bank_app:latest -f ./Dockerfile.postgre .

# Start container
docker compose -f docker-compose.yaml up -d