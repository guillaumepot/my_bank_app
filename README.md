# Personal Bank App

This is a personal project to check my bank accounts. It is currently in development, with plans to add new features in the future.


<img src="./media/bank_app_img.jpeg" width="350" height="350">


---

## Current Features

- Add account (checking, saving, investment)
- Create budgets
- Create transactions & update accounts amounts
- Display charts based on your transactions

---

## Project Information

- **Version**: 0.2.0 - QoL Update
- **Development Stage**: Dev
- **Author**: Guillaume Pot
- **Contact Information**: guillaumepot.pro@outlook.com

---

## Table of Contents
- [Repository Architecture](#repository-architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Changelogs](#Changelogs)
- [Roadmap](#roadmap)

---

## Repository Architecture

```
├── .github
│   │
│   └── workflows < Contains Workflows
|           |
|           ├── .env
|           |
|           └── upload_docker_images.yaml
|   
├── archives < Contains old code files
|       |
|       └── (obsolete)myBankPackage
|
├── build   < Contains builds
|        
├── changelogs < Changelogs for each new version
|        
├── utils < Contains utils py scripts
|     |
|     ├── generate_requirements.py
|     |
|     ├── generate_user_credentials.py
|     |
|     └── requirements.txt
|        
├── dev_test < Development test branch
|
├── media
|       |
|       └── bank_app_img.jpeg
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
├── unit_tests < Contains unit tests
|
├── .env
|
├── .gitignore
│
├── docker-compose.yaml
│
└── README.md
```

---

## Branch logic

```

├── main    # Main branch, contains releases
|   
├── build   # Used to build releases
|
├── debug   # Debug branch
|
└── develop # New features development branch

```

---

## Requirements
- Python with psycopg2, passlib
- Docker
- Docker Compose

---

## Installation
Each step is notified as a comment you can find in the files.


- Step 1: Create a directory for postgres data and attach it as a volume for the postgres container (Step1)
- Step 2: Update the docker-compose file according to your needs.
- Step 3 : Update api.env file according to your needs.



- Step X: Comment port exposure for postgres container



- Add the usernames to AUTHORIZED_USERS var in .env file
- Configure POSTGRES variables in .env file.
- Configure API variables in .env file.


- User docker compose to start services (postgres, api, streamlit UI)
- Use generate_tables.py to generate postgres Database
- Use generate_user_credentials.py to generate new users

---

## Changelogs

[v0.2.1](./changelogs/0.2.1.md)  
[v0.2.0](./changelogs/0.2.0.md)  
[v0.1.3](./changelogs/0.1.3.md)  
[v0.1.2](./changelogs/0.1.2.md)  
[v0.1.1](./changelogs/0.1.1.md)  
[v0.1.0](./changelogs/0.1.0.md)

---

## Roadmap

```
- Streamlit refactorization
- Add Container tests (Github Actions)
- Add more unit tests, e.g., API tests

- Create an ETL pipline to get transaction datas, put raw datas in a storage; transform datas for analytics
- Add analytics charts (based on transactions) -> Analytics page ; Streamlit
- Use a ML pipeline to predict things (budgets, ..)

- Create new category in settings | Streamlit
- Debug transferts
- Update current bdd
- Create init.sql & rmeove script .py | postGres
```