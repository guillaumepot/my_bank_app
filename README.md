# Personal Bank App

This is a personal project to check my bank accounts. It is currently in development, with plans to add new features in the future.


<img src="./media/bank_app_img.jpeg" width="350" height="350">


---


## Project Information

- **Version**: 0.1.2
- **Development Stage**: Development
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
├── changelogs
|       |
|       ├── 0.1.0.md
|       ├── 0.1.0.md
|       └── 0.1.2.md
|        
├── local_tests
|       |
|       ├── set_local_test.sh
|       |
|       └── remove_local_test.sh
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
```

---

## Requirements
- Python
- Docker
- Docker Compose

---

## Installation
- Add a folder for the postgres volume (default: ./storage/postgres_data)
- Add the usernames to AUTHORIZED_USERS var in .env file
- Configure POSTGRES variables in .env file.
- Configure API variables in .env file.


- User docker compose to start services (postgres, api, streamlit UI)
- Use generate_tables.py to generate postgres Database
- Use generate_user_credentials.py to generate new users

---

## Changelogs

[v0.1.2](./changelogs/0.1.2.md)  
[v0.1.1](./changelogs/0.1.1.md)  
[v0.1.0](./changelogs/0.1.0.md)



---

## Roadmap

**[Done]**
```
0.1.2
- Review README.MD
0.1.0
- First version of the app containing an API & a Streamlit interface
0.1.1
- Refactor API files (cleaning & readability)
- Refactor Streamlit files (cleaning & readability)
```


**[Todo]**  
```
0.1.2
- Add a simple logger (API)
- Update API security (max requests, etc.)
- Add Container tests (Github Actions)
- Add more unit tests, e.g., API tests

0.2.0
- Create an ETL pipline to get transaction datas, put raw datas in a storage; transform datas for analytics
- Add analytics charts (based on transactions) -> Analytics page ; Streamlit

0.3.0
- Use a ML pipeline to predict things (budgets, ..)
```
