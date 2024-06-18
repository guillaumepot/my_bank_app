# Personal Bank App

This is a personal project to check my bank accounts. It is currently in development, with plans to add new features in the future.


## Table of Contents
- [Repository Architecture](#repository-architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Logs](#logs)
- [Roadmap](#roadmap)

## Repository Architecture
├── .github
│   │
│   └── workflows
|           |
|           ├── .env
|           |
|           └── upload_docker_images.yaml
|   
├── archives
|       |
|       └── (obsolete)myBankPackage
|        
├── local_tests
|       |
|       ├── set_local_test.sh
|       |
|       └── remove_local_test.sh
|
├── src
|    |
|    ├── api
|    |    |
|    |    ├── api_account_router.py
|    |    |
|    |    ├── api_auth_router.py
|    |    |
|    |    ├── api_budget_router.py
|    |    |
|    |    ├── api_db_connectors.py
|    |    |
|    |    ├── api_main.py
|    |    |
|    |    ├── api_transaction_router.py
|    |    |
|    |    ├── api_vars.py
|    |    |
|    |    ├── Dockerfile
|    |    |
|    |    ├── generate_secret_key.py
|    |    |
|    |    ├── generate_secret_key.sh
|    |    |
|    |    └── requirements.txt
|    |
|    └── streamlit
|         |
|         ├── Dockerfile
|         |
|         ├── requirements.txt
|         |
|         └── streamlit.py
|
├── storage
|     |
|     └── postgres_data
|
├── utils
|     |
|     ├── generate_requirements.py
|     |
|     ├── generate_tables.py
|     |
|     ├── generate_user_credentials.py
|     |
|     └── requirements.txt
|
├── .env
|
├── .gitignore
│
├── docker-compose.yaml
│
└── README.md



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
- Streamlit version: 0.1.1
- Current state: Prod

#### Changelogs
- 0.1.1 :
    - New display for Overview page
    - Added filters
    - Transaction DF now display budget name instead of budget id
    - Removed obsolete "Zoom-in" page
- 0.1.0 :
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