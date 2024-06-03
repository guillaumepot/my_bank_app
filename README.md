# Bank Personal App

This is a personal project to check my bank accounts. It is currently in development, with plans to add new features in the future.

## Table of Contents
- [Repository Architecture](#repository-architecture)
- [Installation](#installation)
- [Additional Information](#additional-information)
- [Roadmap](#roadmap)

## Repository Architecture
[TODO]

## Installation


### Requirements
[TODO]


### User Account
- Use `generate_user_credentials.py` to generate a user account. Your username should be added in `api.env` (AUTHORIZED_USERS).

### PostGres Database
- Configure POSTGRES variables in `postgres.env`.
- User setup & remove scripts to easily start & stop the POSTGRES container.

### API
- Configure API variables in `api.env`.
- Add usernames as AUTHORIZED_USERS.
- Change storage path in docker-compose if needed.
- Use setup & remove scripts to easily start & stop the API container.


### Streamlit
- Configure Streamlit variables in `streamlit.env` (for API communication).
- Use setup & remove scripts to easily start & stop the API container.

## Additional Information

### Package
Package version: 0.1.0
Current state: Production

#### Changelogs
0.1.0 :
    - Package creation

#### Todo
-

### POSTGRES
POSTGRES version: latest
Current state: Dev

#### Changelogs
N/C

### API
API version: 0.1.0
Current state: Production

#### Changelogs
0.1.0 :
    - API creation

#### Todo
- Add logger
- Change directory paths (wait for todo: Data/DB migration)
- /create/account should check if an account already exists instead of erasing it
- /create/budget should check if a budget already exists instead of erasing it

### Streamlit
Streamlit version: 0.1.0
Current state: Production

#### Changelogs
0.1.0 :
    - Streamlit creation

#### Todo
- Add analytics page

### Data (Storage)

#### Todo
- Database migration

## Roadmap
Done:
- First version of the app containing an API & a Streamlit interface

Todo:
- Add analytics (charts)
- Add a ML pipeline to analyze temporal charts
- Add more unit tests, e.g., API tests
- Add Container tests (Github Actions)
- Refactor API files (cleaning & readability)
- Refactor Streamlit files (cleaning & readability)
- Add a logger (API)
- Update API security (max requests, etc.)
- Move objects (accounts, budgets, transactions, users) to RDB

### Git repository
- Add requirements (Docker) and/or furnish other ways to start the app