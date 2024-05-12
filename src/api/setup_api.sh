#!/bin/bash


# Copy myBankPackage
cp -r ../../myBankPackage ./myBankPackage

# Building image
docker build -t personal_bank_app_api:latest -f ./Dockerfile.api .

# Start container
docker-compose -f docker-compose.yaml up -d

# Remove myBankPackage
rm -rf ./myBankPackage