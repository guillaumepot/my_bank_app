#!/bin/bash


# Copy myBankPackage
cp -r ../../myBankPackage ./myBankPackage
# Copy generate_secret_key
cp ../../utils/generate_secret_key.py .
cp ../../utils/generate_secret_key.sh .
chmod +x generate_secret_key.sh

# Building image
docker build -t personal_bank_app_api:latest -f ./Dockerfile.api .

# Start container
docker-compose -f docker-compose.yaml up -d

# Remove myBankPackage
rm -rf ./myBankPackage
rm generate_secret_key.py
rm generate_secret_key.sh