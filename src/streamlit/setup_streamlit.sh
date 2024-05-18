#!/bin/bash

# Create network
docker network create bank_app_network

# Build image
docker build -t personal_bank_app_streamlit:latest -f ./Dockerfile.streamlit .

# Start container
docker-compose -f docker-compose.yaml up -d
