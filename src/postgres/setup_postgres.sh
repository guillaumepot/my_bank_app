#!/bin/bash

# Create network
docker network create bank_app_network

# Start container
docker compose -f docker-compose.yaml up -d