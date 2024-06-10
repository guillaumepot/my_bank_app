#!/bin/sh
export BANK_APP_API_TOKEN_SECRET_KEY=$(python3 generate_secret_key.py)
exec "$@"