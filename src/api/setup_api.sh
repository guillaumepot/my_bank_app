#!/bin/bash


# Generate API Token secret key as an environment variable
export BANK_APP_API_TOKEN_SECRET_KEY=$(python3 ./src/utils/generate_secret_key.py)