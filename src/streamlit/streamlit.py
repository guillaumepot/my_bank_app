"""
### STREAMLIT APP ###
"""
# Version : 0.1.0
# Current state : Dev
# Author : Guillaume Pot
# Contact : guillaumepot.pro@outlook.com


# LIBS
import os
import requests
import pandas as pd
import streamlit as st


# VARS
api_version = os.getenv("API_VERSION")
api_url = os.getenv("API_URL")


api_version = "0.1.0" # TO DELETE WHEN DOCKERIZED
api_url = "http://localhost:8000" # TO DELETE WHEN DOCKERIZED



available_account_types = ["checking", "saving"] # Change to import from API
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
login_data = {}

# Initialize session state
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if "account_type" not in st.session_state:
    st.session_state.account_type = available_account_types[0]
if "name" not in st.session_state:
    st.session_state.name = ""
if "amount" not in st.session_state:
    st.session_state.amount = 0.0

# API STATUS CHECKING
url = f"{api_url}/api/{api_version}/status"
response = requests.get(url)
if response.status_code != 200:
    st.error("Error while checking API status.")
    st.stop()





##### UI #####

### SIDEBAR ###

# Authentication panel
st.sidebar.title("Authentication")
if st.session_state.access_token == None:
    # Login button
        login_placeholder = st.sidebar.empty()
        login_username = st.sidebar.text_input("Username")
        login_password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Log In"):
            login_data = {
                "grant_type": "",
                "username": login_username,
                "password": login_password,
                "scope": "",
                "client_id": "",
                "client_secret": ""
            }
            # Request API
            url = f"{api_url}/api/{api_version}/login"
            response = requests.post(url, data=login_data)
            if response.status_code == 200:
                access_token = response.json().get("access_token")
                st.sidebar.success("Logged In Successfully!")
                login_placeholder.empty()
                st.session_state.access_token = access_token
            else:
                st.sidebar.error("Incorrect Username or Password.")
  
else:
# Logout button
    st.sidebar.empty()
    if st.sidebar.button("Log Out"):
        st.session_state.pop('access_token', None)
    st.sidebar.empty()

# Navigation
st.sidebar.title("Personal bank app")

# Pages
pages=["Overview", "Zoom-in", "Settings"]
page=st.sidebar.radio("Navigation", pages)


## END OF SIDEBAR ##





### MAIN UI ###
# Overview page
if page == pages[0]:
    st.title("Overview")
   

    if st.button("Display all accounts", key="display_accounts_button"):
        # Get account table
        url = f"{api_url}/api/{api_version}/table/account"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {st.session_state.access_token}"
            }        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            st.error("Error while requesting API.")
            response.status_code
        else:
            df = pd.DataFrame(response.json())
        # Save df to session state
        st.session_state.df_accounts = df

    # Check if df is in session state
    if 'df_accounts' in st.session_state:
        # Sortby button
        sort_by = st.selectbox('Sort by:', st.session_state.df_accounts.columns, key="sort_by_accounts")
        sorted_df = st.session_state.df_accounts.sort_values(sort_by)
        st.table(sorted_df)



    if st.button("Display all budgets", key="display_budgets_button"):
        # Get budget table
        url = f"{api_url}/api/{api_version}/table/budget"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {st.session_state.access_token}"
            }        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            st.error("Error while requesting API.")
            response.status_code
        else:    
            df = pd.DataFrame(response.json())
        # Save df to session state
        st.session_state.df_budgets = df

    # Check if df is in session state
    if 'df_budgets' in st.session_state:
        # Sortby button
        sort_by = st.selectbox('Sort by:', st.session_state.df_budgets.columns, key="sort_by_budgets")
        sorted_df = st.session_state.df_budgets.sort_values(sort_by)
        st.table(sorted_df)




# Zoom-in page
if page == pages[1]: 
    st.session_state.pop('df_budgets', None)
    st.session_state.pop('df_accounts', None)
    st.title("Zoom In")
    
    choice = st.selectbox("Display", ["Accounts", "Budgets", "Transactions"], key='choice_display_object')

    if choice == "Accounts":
        url = f"{api_url}/api/{api_version}/get/accounts" # Change /get/account to /get/accounts
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {st.session_state.access_token}"
            }     
        response = requests.get(url, headers=headers)
        available_accounts = (elt for elt in response.json())
        account_choice = st.selectbox("Choose a budget", available_accounts)
        st.write(account_choice) # Change to get specific budget informations (add API route)
        
    if choice == "Budgets":
        url = f"{api_url}/api/{api_version}/get/budgets"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {st.session_state.access_token}"
            }     
        response = requests.get(url, headers=headers)
        available_budgets = (elt for elt in response.json())
        budget_choice = st.selectbox("Choose a budget", available_budgets)
        st.write(budget_choice) # Change to get specific budget informations (add API route)


    if choice == "Transactions":
        st.write("Not implemented yet.")
        pass # TO BE IMPLEMENTED






# Settings page
if page == pages[2]: 
    st.session_state.pop('df_budgets', None)
    st.session_state.pop('df_accounts', None)
    st.title("Settings")
    st.write("This is the settings page, use the options below to change the settings of the app.")


    # Settings
    if st.button("Check API status", key="check_api_status_button"):
        # Request API
        url = f"{api_url}/api/{api_version}/status"
        response = requests.get(url)
        if response.status_code == 200:
            st.success(response.json())
        else:
            st.error("An error occurred while checking the API status.")


    col_account, col_budget = st.columns(2)
    # Create account
    with col_account:
        with st.form(key="create_account_form"):
            # Add account informations
            st.subheader("Please fill in the form below to create an account.")
            st.write("Name is free text")
            name = st.text_input(label="Account name")
            account_type = st.selectbox("Choose account type", available_account_types, key="account_type")
            amount = st.number_input("Amount", format="%.2f", key="amount_account_input")
            submit_button = st.form_submit_button(label='Create Account')

        if submit_button:
            # Request API
            access_token = st.session_state.access_token
            if access_token:
                url = f"{api_url}/api/{api_version}/create/account?name={name}&type={account_type}&amount={amount}"
                headers = {
                    "accept": "application/json",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Bearer {st.session_state.access_token}"
                    }        
                response = requests.post(url, headers=headers)
                if response.status_code == 200:
                    st.success(response.json())
                else:
                    st.error("An error occurred.")
                    st.write(response)

            else:
                st.error("Please Log In to create an account.")

    # Create budget
    with col_budget:
        with st.form(key="create_budget_form"):
            # Add budget informations
            st.subheader("Please fill in the form below to create a budget.")
            st.write("Name is free text")
            name = st.text_input(label="Budget name")
            budget_month = st.selectbox("Choose month", months, key="budget_month")
            amount = st.number_input("Amount", format="%.2f", key="amount_budget_input")
            submit_button = st.form_submit_button(label='Create Budget')

        if submit_button:
            # Request API
            access_token = st.session_state.access_token
            if access_token:
                headers = {
                    "accept": "application/json",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Bearer {st.session_state.access_token}"
                    }        
                url = f"{api_url}/api/{api_version}/create/budget?name={name}&month={budget_month}&amount={amount}"
                response = requests.post(url, headers=headers)
                if response.status_code == 200:
                    st.success(response.json())
                else:
                    st.error("An error occurred.")
                    st.write(response)

            else:
                st.error("Please Log In to create an account.")



### SIDEBAR FOOTER ###
def addSidebarFooter():
    st.markdown("""
        <style>
        .reportview-container .main footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)

    footer="""
     <footer style="margin-top: 350px;">
        <p>Author: Guillaume Pot</p>
        <p>Email: <a href="mailto:guillaumepot.pro@outlook.com">guillaumepot.pro@outlook.com</a></p>
        <p>LinkedIn: <a href="https://www.linkedin.com/in/062guillaumepot/" target="_blank">Click Here</a></p>
    </footer>
    """
    st.sidebar.markdown(footer, unsafe_allow_html=True)

addSidebarFooter()