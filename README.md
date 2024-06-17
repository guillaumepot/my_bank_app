# Personal Bank App

This is a personal project to check my bank accounts. It is currently in development, with plans to add new features in the future.


## Table of Contents
- [Repository Architecture](#repository-architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Logs](#logs)
- [Roadmap](#roadmap)

## Repository Architecture
[TODO]




## Requirements
- Python
- Docker
- Docker Compose




## Installation
- Add a folder for the postgres volume (default: ./storage/postgres_data)
- Add the usernames to AUTHORIZED_USERS var in .env file
- Configure POSTGRES variables in .env file.
- Configure API variables in .env file.


- User docker compose to start services (postgres, api, streamlit UI)
- Use generate_tables.py to generate postgres Database
- Use generate_user_credentials.py to generate new users



## Logs

### POSTGRES
- POSTGRES version 14
- Current state: Prod



### API
- API version: 0.1.0
- Current state: Prod

#### Changelogs
0.1.0 :
    - API creation

#### Todo
- Add logger


### Streamlit
- Streamlit version: 0.2.0
- Current state: Prod

#### Changelogs
0.1.0 :
    - Streamlit creation

#### Todo
- 



## Roadmap
[Done]
- First version of the app containing an API & a Streamlit interface
- Refactor API files (cleaning & readability)
- Refactor Streamlit files (cleaning & readability)

[Todo]
- Create an ETL pipline to get transaction datas
- Add analytics charts (based on transactions) -> Analytics page ; Streamlit
- Use a ML pipeline to predict things (budgets, ..)
- Add more unit tests, e.g., API tests
- Add Container tests (Github Actions)
- Add a logger (API)
- Update API security (max requests, etc.)