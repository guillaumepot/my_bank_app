# Bank personal app

This is a personal project to check my bank accounts.
Currently in dev state, I plan to add new features in the future.


## Repo Architecture
[TODO]



## INSTALL

### User account
- Use generate_user_credentials.py to generate a user account. Your username should be added in api.env (AUTHORIZED_USERS)


### API
- Configure API vars in api.env
- Add usernames as AUTHORIZED_USERS
- Change storage path in docker-compose if needed
- Use setup & remove scripts to start & stop API container easily.

### Streamlit
- Configure Streamlit vars in streamlit.env (for API communication)
- Use setup & remove scripts to start & stop API container easily.




## Additional Informations
### Package
Package version : 0.1.0
Current state : Prod


#### Changelogs
0.1.0 :
    - Package creation

#### Todo
-




### API
Api version : 0.1.0
Current state : Prod

#### Changelogs
0.1.0 :
    - API creation


#### Todo
- Add logger
- Change dir paths (wait for todo:Datas/DB migration)
- /create/account should check if an account already exists instead of erasing it
- /create/budget should check if a budget already exists instead of erasing it



### Streamlit
Steamlit version : 0.1.0
Current state : Prod


#### Changelogs
0.1.0 :
    - Streamlit creation

#### Todo
- Add analytics page



### Datas (storage)

#### Todo
- DB migration





## Roadmap
Done :
- First version of the app containing an API & a Streamlit interface


Todo :
- Add analytics (charts)
- Add a ML pipeline to a analyse temporal charts
- Add more unit tests, ex: api tests
- Add Container tests (Github Actions)
- Refactorize API files (cleaning & readability)
- Refactorize Streamlit files (cleaning & readability)
- Add a logger (API)
- Update API security (max requests, ..)
- Move objects (accounts, budgets, transactions, users) to RDB