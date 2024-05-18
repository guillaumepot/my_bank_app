"""
### STREAMLIT APP ###
"""
# Version : 0.1.1
# Current state : Dev
# Author : Guillaume Pot
# Contact : guillaumepot.pro@outlook.com


# LIBS
import os
import requests
import pandas as pd
import streamlit as st


# VARS
api_version = os.getenv("API_VERSION", "0.1.0")
api_url = os.getenv("API_URL", "http://localhost:8000")


months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
login_data = {}



# Initialize session state
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
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
if st.session_state.access_token == None:
    st.error("Please Log In to access the app.")
    st.stop()
pages=["Overview", "Zoom-in", "Transactions", "Settings"]
page=st.sidebar.radio("Navigation", pages)


## END OF SIDEBAR ##


### API HEADER AUTHORIZATION ###
st.session_state.headers = {
    "accept": "application/json",
    'Content-Type': 'application/json',    
    #"Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Bearer {st.session_state.access_token}"
    }        





### MAIN UI ###
# Overview page
if page == pages[0]:
    st.title("Overview")
   
    # Get account table
    url = f"{api_url}/api/{api_version}/table/account"
    response = requests.get(url, headers=st.session_state.headers)
    if response.status_code != 200:
        st.error("Error while requesting API.")
        response.status_code
        st.stop()
    else:
        if response.json() == []:
            st.warning("No data available.")
            st.stop()
        df = pd.DataFrame(response.json())
        df["amount"] = df["amount"].apply(lambda x: f"{x:.2f} €")
        df.drop(columns=["id", "history"], inplace=True)
        # Save df to session state
        st.session_state.df_accounts = df

        st.subheader("Accounts")
        filter_col, sortby_col = st.columns(2)

        # Filter button
        with filter_col:
            filters = [x for x in st.session_state.df_accounts.type.unique()]
            filters.insert(0, "")
            filter_value = st.selectbox('Filter type:', filters, key="filter_by_accounts")
            if filter_value != "":
                st.session_state.df_accounts = st.session_state.df_accounts[st.session_state.df_accounts["type"] == filter_value]

        # Sort by button
        with sortby_col:
            sort_by = st.selectbox('Sort by:', st.session_state.df_accounts.columns, key="sort_by_accounts")
            st.session_state.df_accounts = st.session_state.df_accounts.sort_values(sort_by)

        st.table(st.session_state.df_accounts)


    # Get budget table
    url = f"{api_url}/api/{api_version}/table/budget"    
    response = requests.get(url, headers=st.session_state.headers)
    if response.status_code != 200:
        st.error("Error while requesting API.")
        response.status_code
        st.stop()
    else: 
        if response.json() == []:
            st.warning("No data available.")
            st.stop()
        df = pd.DataFrame(response.json())
        df["amount"] = df["amount"].apply(lambda x: f"{x:.2f} €")
        df.drop(columns=["id", "history"], inplace=True)
        # Save df to session state
        st.session_state.df_budgets = df

        st.subheader("Budgets")
        filter_col, sortby_col = st.columns(2)

        # Filter button
        with filter_col:
            filters = [x for x in st.session_state.df_budgets.month.unique()]
            filters.insert(0, "")
            filter_value = st.selectbox('Filter month:', filters, key="filter_by_budgets")
            if filter_value != "":
                st.session_state.df_budgets = st.session_state.df_budgets[st.session_state.df_budgets["month"] == filter_value]

        # Sort by button
        with sortby_col:
            sort_by = st.selectbox('Sort by:', st.session_state.df_budgets.columns, key="sort_by_budgets")
            st.session_state.df_budgets = st.session_state.df_budgets.sort_values(sort_by)

        st.table(st.session_state.df_budgets)




# Zoom-in page
if page == pages[1]: 
    st.session_state.pop('df_budgets', None)
    st.session_state.pop('df_accounts', None)
    st.title("Zoom In")
    
    choice = st.selectbox("Display", ["Accounts", "Budgets", "Transactions"], key='choice_display_object')

    if choice == "Accounts":
        # Get account table
        url = f"{api_url}/api/{api_version}/table/account"
        response = requests.get(url, headers=st.session_state.headers)
        if response.status_code != 200:
            st.error("Error while requesting API.")
            response.status_code
            st.stop()
        else:
            df = pd.DataFrame(response.json())
            df["amount"] = df["amount"].apply(lambda x: f"{x:.2f} €")
            # Save df to session state
            st.session_state.df_accounts = df

        account_choice = st.selectbox("Choose an account", st.session_state.df_accounts["name"].values)
        account_to_display = st.session_state.df_accounts[st.session_state.df_accounts["name"] == account_choice]

        st.write(account_to_display["name"].values[0])
        for col in account_to_display.columns[1:4]:
            st.write(f"{col}: {account_to_display[col].values[0]}")
        st.write("**History**")
        account_history = account_to_display["history"].values[0]
        if account_history == []:
            st.write("No history available.")
            st.stop()
        account_history_df = pd.DataFrame(account_history)
        account_history_df["amount"] = account_history_df["amount"].apply(lambda x: f"{x:.2f} €")
        st.dataframe(account_history_df)

    if choice == "Budgets":
        # Get budget table
        url = f"{api_url}/api/{api_version}/table/budget"
        response = requests.get(url, headers=st.session_state.headers)

        # If status code is not 200
        if response.status_code != 200:
            st.error("Error while requesting API.")
            response.status_code
            st.stop()

        # If status code is 200
        else:
            df = pd.DataFrame(response.json())
            df["amount"] = df["amount"].apply(lambda x: f"{x:.2f} €")
            # Save df to session state
            st.session_state.df_budgets = df
        

        # Display budget
        # Month Choice
        available_months = st.session_state.df_budgets["month"].unique()
        month_choice = st.selectbox("Choose a month", available_months)
        st.session_state.df_budgets = st.session_state.df_budgets[st.session_state.df_budgets["month"] == month_choice]

        # Budget Choice
        budget_choice = st.selectbox("Choose a budget", st.session_state.df_budgets["name"].values)
        budget_to_display = st.session_state.df_budgets[st.session_state.df_budgets["name"] == budget_choice]

        st.write(budget_to_display["name"].values[0])
        for col in budget_to_display.columns[1:4]:
            st.write(f"{col}: {budget_to_display[col].values[0]}")
        st.write("**History**")
        budget_history = budget_to_display["history"].values[0]
        if budget_history == []:
            st.write("No history available.")
            st.stop()
        budget_history_df = pd.DataFrame(budget_history)
        budget_history_df["amount"] = budget_history_df["amount"].apply(lambda x: f"{x:.2f} €")
        st.dataframe(budget_history_df)



    if choice == "Transactions":
        # Get transaction table
        url = f"{api_url}/api/{api_version}/table/transaction"
        response = requests.get(url, headers=st.session_state.headers)

        # If status code is not 200
        if response.status_code != 200:
            st.error("Error while requesting API.")
            response.status_code
            st.stop()

        # If status code is 200
        else:
            transaction_table = response
            transaction_table = pd.DataFrame(transaction_table.json())
            transaction_table["amount"] = transaction_table["amount"].apply(lambda x: f"{x:.2f} €")
            st.subheader("Transaction table")
            # Search bar for transaxction id
            search = st.text_input("Search by transaction id")
            if search:
                transaction_table = transaction_table[transaction_table["id"] == search]
            st.dataframe(transaction_table)




# Transactions page
if page == pages[2]: 
    st.session_state.pop('df_budgets', None)
    st.session_state.pop('df_accounts', None)
    if "transaction_datas" in st.session_state:
        st.session_state.pop('transaction_datas', None)


    st.title("Transactions")

    # Get available transaction types
    url = f"{api_url}/api/{api_version}/available/transaction_types"
    available_transaction_types = requests.get(url, headers=st.session_state.headers)
    available_transaction_types = available_transaction_types.json()
    available_transaction_types = [elt for elt in available_transaction_types]

    # Get available accounts
    url = f"{api_url}/api/{api_version}/get/account"
    response = requests.get(url, headers=st.session_state.headers)
    response_json = response.json()
    available_accounts = [account.split('.pkl')[0] for account in response_json.get('available accounts', [])]
    available_accounts.insert(0, None)

    # Get available budgets
    url = f"{api_url}/api/{api_version}/get/budget"
    response = requests.get(url, headers=st.session_state.headers)
    response_json = response.json()
    available_budgets = [budget.split('.pkl')[0] for budget in response_json.get('available budgets', [])]
    available_budgets.insert(0, None)


    # Add a transactions
    with st.form(key="create_transaction_form"):
        # Add transaction informations
        st.subheader("Please fill in the form below to create a transaction.")
        transaction_date = st.date_input("Transaction date", key="transaction_date")
        transaction_date = str(transaction_date)
        transaction_type = st.selectbox("Choose transaction type", available_transaction_types, key="transaction_type")
        transaction_amount = st.number_input("Amount", format="%.2f", key="amount_account_input")

        datas = {
            "date": transaction_date,
            "type": transaction_type,
            "amount": transaction_amount
            }

        origin_account = st.selectbox("Choose origin account", available_accounts, key="origin_account")

        if origin_account != None:
            datas["origin_account"] = origin_account


        destination_account = st.selectbox("Choose destination account", available_accounts, key="destination_account")

        if destination_account:
            datas["destination_account"] = destination_account


        budget = st.selectbox("Choose budget", available_budgets, key="budget_transaction")
        budget = None if budget == "None" else budget
        if budget is not None:
            budget_name = budget.split("_")[0]

        budget_month = budget.split("_")[1] if budget != None else None

        if budget:
            datas["budget"] = budget_name
            datas["budget_month"] = budget_month


        description = st.text_input("description", key="transaction_description")

        datas["description"] = description


        submit_button = st.form_submit_button(label='Create Transaction')

    if submit_button:
        # Request API
        access_token = st.session_state.access_token
        if access_token:
            st.write(datas)
            url = f"{api_url}/api/{api_version}/create/transaction"
            response = requests.post(url, headers=st.session_state.headers, params=datas)

            # Add transaction to seesion_state
            if response.status_code == 200:
                st.session_state.transaction_datas = response.json()
                st.success(f"Transaction created: \n {st.session_state.transaction_datas}")                             

            # If status code is not 200
            else:
                st.write(response.json())
         
        # If no access token
        else:
            st.error("Please Log In to create a transaction.")
            st.write(response.json())





# Settings page
if page == pages[3]: 
    st.session_state.pop('df_budgets', None)
    st.session_state.pop('df_accounts', None)
    st.title("Settings")
    st.write("This is the settings page, use the options below to change the settings of the app.")

    # Get available account types
    url = f"{api_url}/api/{api_version}/available/account_types"
    available_account_types = requests.get(url, headers=st.session_state.headers)
    available_account_types = available_account_types.json()
    available_account_types = [elt for elt in available_account_types]

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
                response = requests.post(url, headers=st.session_state.headers)
                
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
                url = f"{api_url}/api/{api_version}/create/budget?name={name}&month={budget_month}&amount={amount}"
                response = requests.post(url, headers=st.session_state.headers)
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