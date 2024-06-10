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
- Setup PostGres DB Container
- Generate Tables
- Generate User
- Setup API container
- Setup Streamlit container




### Requirements
[TODO]
- Docker
- 

### User Account
- Use `generate_user_credentials.py` to generate a user account. Your username should be added in `api.env` (AUTHORIZED_USERS).

### PostGres Database
- Configure POSTGRES variables in `postgres.env`.
- User setup & remove scripts to easily start & stop the POSTGRES container.
- Generate tables using the script 'generate_tables'
- Add a user using the script 'generate_user_credentials'

### API
- Configure API variables in `api.env`.
- Add usernames as AUTHORIZED_USERS.
- Change storage path in docker-compose if needed.
- Use setup & remove scripts to easily start & stop the API container.


### Streamlit
- Configure Streamlit variables in `streamlit.env` (for API communication).
- Use setup & remove scripts to easily start & stop the API container.



## Additional Information


#### Todo
-

### POSTGRES
POSTGRES version: 0.1.1 (postgres 14)
Current state: Prod

#### Changelogs
0.1.0 :
    - Docker compose creation
0.1.1 :
    - Update postgres:13 to postgres:14
    - Docker compose minor update (add env var POSTGRES_PORT)




### API
API version: 0.1.0
Current state: Prod

#### Changelogs
0.1.0 :
    - API creation
0.2.0 :
    - Major update
        - API code refactorization
        - Code migration (package to PostgresDB)
*
#### Todo
- Add logger

### Streamlit
Streamlit version: 0.2.0
Current state: Prod


#### Changelogs
0.1.0 :
    - Streamlit creation
0.2.0 :
    - Major Update:
        - Streamlit code refactorization
        

#### Todo
- 


### Data (Storage)

#### Todo
- [Done] Database migration 



## Roadmap
[Done]
- First version of the app containing an API & a Streamlit interface
- Refactor API files (cleaning & readability)
- Refactor Streamlit files (cleaning & readability)

[Todo]
- Add analytics (charts)
- Add a ML pipeline to analyze temporal charts
- Add more unit tests, e.g., API tests
- Add Container tests (Github Actions)
- Add a logger (API)
- Update API security (max requests, etc.)


### Git repository
- Add requirements (Docker) and/or furnish other ways to start the app