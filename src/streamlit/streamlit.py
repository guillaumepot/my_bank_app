"""
### STREAMLIT APP - Main file ###
"""
# Version : 0.1.1
# Current state : Prod
# Author : Guillaume Pot
# Contact : guillaumepot.pro@outlook.com


# LIBS
import os
import requests
import calendar
import pandas as pd
import streamlit as st


# VARS
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
login_data = {}
elt_to_display = ["All", "1", "5", "10", "15", "30", "50"]


# API VARS
api_version = os.getenv("API_VERSION", "0.1.0")
api_url = os.getenv("API_URL", "http://localhost:8000")

# API STATUS CHECKING
url = f"{api_url}/api/{api_version}/status"
response = requests.get(url)
if response.status_code != 200:
    st.error("Error while checking API status.")
    st.stop()


# Initialize session state
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'selected_account' not in st.session_state:
    st.session_state['selected_account'] = {
        'id': None,
        'name': None,
        'type': None,
        'balance': None
    }



### SIDEBAR ###

# Navigation
st.sidebar.title("Personal bank app")

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
                st.sidebar.empty()

            else:
                st.sidebar.error("Incorrect Username or Password.")
  
else:
# Logout button
    st.sidebar.empty()
    if st.sidebar.button("Log Out", key="sidebar_logout_button"):
        st.session_state.pop('access_token', None)
        st.rerun()


# Pages (Displayed only if logged in)
if st.session_state.access_token == None:
    st.error("Please Log In to access the app.")
    st.stop()
pages=["Overview", "Transactions", "Analytics", "Settings"]
page=st.sidebar.radio("Navigation", pages)

## END OF SIDEBAR ##



### API HEADER AUTHORIZATION ###
st.session_state.headers = {
    "accept": "application/json",
    'Content-Type': 'application/json',    
    #"Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Bearer {st.session_state.access_token}"
    }        




### PAGES ###

# Overview
if page == pages[0]:
    st.title("Overview")


    ## Get Tables


    # Get account table
    url = f"{api_url}/api/{api_version}/table/account"
    account_table = requests.get(url, headers=st.session_state.headers)
    account_table = dict(account_table.json())
    account_table = account_table['account table']
    # Generate DF
    df_accounts = pd.DataFrame(account_table, columns=["id", "name", "type", "balance", "owner_id", "created_at"])
    df_accounts["balance"] = df_accounts["balance"].apply(lambda x: f"{x:.2f} €")
    df_accounts.drop(columns=["id", "owner_id"], inplace=True)
    df_accounts["created_at"] = df_accounts["created_at"].str.split("T").str[0]


    # Get budget table
    url = f"{api_url}/api/{api_version}/table/budget"
    budget_table = requests.get(url, headers=st.session_state.headers)
    budget_table = budget_table.json()
    budget_table = budget_table["budget table"]
    # Generate DF
    df_budgets = pd.DataFrame(budget_table, columns=["id", "name", "month", "amount","created_at"])
    df_budgets["amount"] = df_budgets["amount"].apply(lambda x: f"{x:.2f} €")

    # Create a dictionary mapping from id to name in df_budgets (used for df_transactions)
    budget_id_to_name = pd.Series(df_budgets.name.values, index=df_budgets.id).to_dict()

    df_budgets.drop(columns=["id"], inplace=True)
    df_budgets["created_at"] = df_budgets["created_at"].str.split("T").str[0]


    # Get transaction table
    url = f"{api_url}/api/{api_version}/table/transaction"
    transaction_table = requests.get(url, headers=st.session_state.headers)
    transaction_table = dict(transaction_table.json())
    transaction_table = transaction_table['transaction table']
    # Generate DF
    df_transactions = pd.DataFrame(transaction_table, columns=["id", "date", "type", "amount", "origin_account", "destination_account", "budget", "recipient", "category", "description"])
    df_transactions["date"] = df_transactions["date"].str.split("T").str[0]
    df_transactions["amount"] = df_transactions["amount"].apply(lambda x: f"{x:.2f} €")

    # Map each budget id in df_transactions to its corresponding name using the dictionary
    df_transactions["budget_name"] = df_transactions["budget"].map(budget_id_to_name).fillna("None")
    df_transactions.drop(columns=["id", "budget"], inplace=True)
    df_transactions.rename(columns={"budget_name": "budget"}, inplace=True)
    df_transactions = df_transactions[["date", "type", "amount", "origin_account", "destination_account", "budget", "recipient", "category", "description"]]




    ## Display Accounts
    st.subheader("Accounts")

    # Filters
    with st.expander("Account Filters"):
        elt_to_display_col, filter_col, sortby_col = st.columns(3)

        # Elt to display button
        with elt_to_display_col:
            filters = [x for x in elt_to_display]
            filter_value = st.selectbox('Display:', filters, key="nb_elts_to_display_by_accounts")
            if filter_value != "All":
                df_accounts = df_accounts.head(int(filter_value))

        # Filter button
        with filter_col:
            filters = [x for x in df_accounts.type.unique()]
            filters.insert(0, "")
            filter_value = st.selectbox('Filter type:', filters, key="filter_by_accounts")
            if filter_value != "":
                df_accounts = df_accounts[df_accounts["type"] == filter_value]

        # Sort by button
        with sortby_col:
            sort_by = st.selectbox('Sort by:', df_accounts.columns, key="sort_by_accounts")
            df_accounts = df_accounts.sort_values(sort_by)

    # Interactive display of accounts
    with st.expander("View Accounts"):
        st.dataframe(df_accounts)
        total_displayed_accounts_amount = df_accounts["balance"].apply(lambda x: float(x.split(" ")[0])).sum()
        st.markdown(f"**Total amount in displayed accounts:** {total_displayed_accounts_amount:.2f} €", unsafe_allow_html=True)




    ## Display Budgets
    st.subheader("Budgets")

    
    # Filters
    with st.expander("Budget Filters"):
        elt_to_display_col, filter_col, sortby_col = st.columns(3)

        # Elt to display button
        with elt_to_display_col:
            filters = [x for x in elt_to_display]
            filter_value = st.selectbox('Display:', filters, key="nb_elts_to_display_by_budgets")
            if filter_value != "All":
                df_budgets = df_budgets.head(int(filter_value))

        # Filter button
        with filter_col:
            filters = ["name", "month"]
            filters.insert(0, "")
            filter_value = st.selectbox('Filter by:', filters, key="filter_by_budgets")

            if filter_value == "name":
                available_budget_names = df_budgets["name"].unique()
                filter_value = st.selectbox('Filter by name:', available_budget_names, key="filter_by_budgets_name")
                df_budgets = df_budgets[df_budgets["name"] == filter_value]


            if filter_value == "month":
                filter_value = st.selectbox('Filter by month:', months, key="filter_by_budgets_month")
                df_budgets = df_budgets[df_budgets["month"] == filter_value]


        # Sort by button
        with sortby_col:
            sort_by = st.selectbox('Sort by:', df_budgets.columns, key="sort_by_budgets")
            df_budgets = df_budgets.sort_values(sort_by)

    # Interactive display of budgets
    with st.expander("View Budgets"):
        st.dataframe(df_budgets)
        total_displayed_budgets_amount = df_budgets["amount"].apply(lambda x: float(x.split(" ")[0])).sum()
        st.markdown(f"**Total amount in displayed budgets:** {total_displayed_budgets_amount:.2f} €", unsafe_allow_html=True)



    ## Display Transactions
    st.subheader("Transactions")

    # Filters
    with st.expander("Transaction Filters"):
        elt_to_display_col, sortby_col, filter_col = st.columns(3)

        # Elt to display button
        with elt_to_display_col:
            filters = [x for x in elt_to_display]
            filter_value = st.selectbox('Display:', filters, key="nb_elts_to_display_by_transactions")
            if filter_value != "All":
                df_transactions = df_transactions.head(int(filter_value))


        # Sort by button
        with sortby_col:
            sort_by = st.selectbox('Sort by:', df_transactions.columns, key="sort_by_transactions")
            df_transactions = df_transactions.sort_values(sort_by)


        # Filter button
        with filter_col:
            # Initialize available filters
            selected_filters = {
                "month": None,
                "type": None,
                "origin_account": None,
                "destination_account": None,
                "budget": None,
                "recipient": None,
                "category": None
            }

            # Display checkboxes for each filter
            for filter_name in selected_filters.keys():
                if st.checkbox(f'Filter by {filter_name}', key=f'checkbox_{filter_name}'):
                    # Display filter options based on filter_name
                    if filter_name == "month":
                        df_transactions["date"] = pd.to_datetime(df_transactions["date"])
                        df_transactions["month"] = df_transactions["date"].dt.month
                        unique_months = df_transactions["month"].unique()
                        unique_months.sort()
                        unique_months_names = [calendar.month_name[month] for month in unique_months]
                        selected_filters[filter_name] = st.multiselect('Select month(s):', unique_months_names, key=f'select_{filter_name}')

                    if filter_name == "type":
                        selected_filters[filter_name] = st.multiselect('Filter by type:', df_transactions["type"].unique(), key=f'select_{filter_name}')

                    if filter_name == "origin_account":
                        selected_filters[filter_name] = st.multiselect('Filter by origin account:', df_transactions["origin_account"].unique(), key=f'select_{filter_name}')

                    if filter_name == "destination_account":
                        selected_filters[filter_name] = st.multiselect('Filter by destination account:', df_transactions["destination_account"].unique(), key=f'select_{filter_name}')

                    if filter_name == "budget":
                        selected_filters[filter_name] = st.multiselect('Filter by budget:', df_transactions["budget"].unique(), key=f'select_{filter_name}')

                    if filter_name == "recipient":
                        selected_filters[filter_name] = st.multiselect('Filter by recipient:', df_transactions["recipient"].unique(), key=f'select_{filter_name}')

                    if filter_name == "category":
                        selected_filters[filter_name] = st.multiselect('Filter by category:', df_transactions["category"].unique(), key=f'select_{filter_name}')


            # Apply filters sequentially
            for filter_name, filter_value in selected_filters.items():
                if filter_value:
                    # Apply filter based on filter_name
                    if filter_name == "month":
                        month_to_num = {month: index for index, month in enumerate(calendar.month_name) if month}
                        filter_value_nums = [month_to_num[month] for month in filter_value]
                        df_transactions = df_transactions[df_transactions["month"].isin(filter_value_nums)]

                    if filter_name == "type":
                        df_transactions = df_transactions[df_transactions["type"].isin(filter_value)]
                    
                    if filter_name == "origin_account":
                        df_transactions = df_transactions[df_transactions["origin_account"].isin(filter_value)]
                    
                    if filter_name == "destination_account":
                        df_transactions = df_transactions[df_transactions["destination_account"].isin(filter_value)]
                    
                    if filter_name == "budget":
                        df_transactions = df_transactions[df_transactions["budget"].isin(filter_value)]
                    
                    if filter_name == "recipient":
                        df_transactions = df_transactions[df_transactions["recipient"].isin(filter_value)]

                    if filter_name == "category":
                        df_transactions = df_transactions[df_transactions["category"].isin(filter_value)]


    # Interactive display of transactions
    with st.expander("View Transactions"):
        st.dataframe(df_transactions)
        total_displayed_transactions_amount = df_transactions["amount"].apply(lambda x: float(x.split(" ")[0])).sum()
        st.markdown(f"**Total amount in displayed accounts:** {total_displayed_transactions_amount:.2f} €", unsafe_allow_html=True)



### END OF PAGE: OVERVIEW ###




### TRANSACTIONS ###


# Transactions
if page == pages[1]: 
    st.title("Transactions")

    # Create transaction form
    with st.form(key="create_transaction_form"):

        # Get available transaction types
        url = f"{api_url}/api/{api_version}/available/transaction_types"
        available_transaction_types = requests.get(url, headers=st.session_state.headers)
        available_transaction_types = available_transaction_types.json()

        # Get available accounts
        url = f"{api_url}/api/{api_version}/table/account"
        account_table = requests.get(url, headers=st.session_state.headers)
        account_table = account_table.json()
        account_table = account_table["account table"]
        account_names = [account[1] for account in account_table]
        account_names.insert(0, "None")
    
        # Get available budgets
        url = f"{api_url}/api/{api_version}/table/budget"
        budget_table = requests.get(url, headers=st.session_state.headers)
        budget_table = budget_table.json()
        budget_table = budget_table["budget table"]
        budget_names = [budget[1] for budget in budget_table]
        budget_names.insert(0, "None")
        budget_months = [budget[2] for budget in budget_table]
        budget_months.insert(0, "None")


        # Form
        st.subheader("Please fill in the form below to create a transaction.")

        transaction_date = st.date_input("Transaction date", key="transaction_date")
        transaction_date = str(transaction_date)
        transaction_type = st.selectbox("Choose transaction type", available_transaction_types, key="available_transaction_type")
        transaction_amount = st.number_input("Amount", format="%.2f", key="amount_transaction_input")
        transaction_origin_account = st.selectbox("Choose origin account", account_names, key="transaction_origin_account")
        transaction_destination_account = st.selectbox("Choose destination account", account_names, key="transaction_destination_account")
        budget_name = st.selectbox("Choose budget", budget_names, key="transaction_budget_name")
        budget_month = st.selectbox("Choose month", budget_months, key="transaction_budget_month")
        transaction_recipient = st.text_input(label="Transaction Recipient")
        category = st.text_input(label="Transaction Category")
        description = st.text_input(label="Transaction Description")

        submit_button = st.form_submit_button(label='Create Transaction')


        # Request API when submit button is clicked
        if submit_button:

            url = f"{api_url}/api/{api_version}/create/transaction"
            params = {
                "transaction_date": transaction_date.strip(),
                "transaction_type": transaction_type.strip(),
                "transaction_amount": transaction_amount,
                "origin_account": transaction_origin_account.strip(),
                "destination_account": transaction_destination_account.strip(),
                "budget_name": budget_name.strip(),
                "budget_month": budget_month.strip(),
                "recipient": transaction_recipient.strip(),
                "category": category.strip(),
                "description": description.strip()
            }
            response = requests.post(url, params=params, headers=st.session_state.headers)
            if response.status_code == 200:
                st.success(response.json())
            else:
                st.error("An error occurred.")


### END OF PAGE: TRANSACTIONS ###


### ANALYTICS ###
if page == pages[2]: 
    st.title("Analytics")
    st.warning("Not implemented yet")

### END OF PAGE: ANALYTICS ###





### SETTINGS ###
if page == pages[3]:
    st.title("Settings")
    st.write("This is the settings page, use the options below to change the settings of the app.")

    # Check API Status button
    if st.button("Check API status", key="check_api_status_button"):
        # Request API
        url = f"{api_url}/api/{api_version}/status"
        response = requests.get(url)
        if response.status_code == 200:
            st.success(response.json())
        else:
            st.error("An error occurred while checking the API status.")

    # Divide in two columns, one for accounts and one for budgets
    col_account, col_budget = st.columns(2)

    # Account Column
    with col_account:
        # Button to choose : Create | Delete (account)
        create_delete_choice_account = st.radio("Choose", ["Create Account", "Delete Account"], key="create_delete_choice_account")
        
        # Create account choice
        if create_delete_choice_account == "Create Account":
            with st.form(key="create_account_form"):

                # Get available account types
                url = f"{api_url}/api/{api_version}/available/account_types"
                available_account_types = requests.get(url, headers=st.session_state.headers)
                available_account_types = available_account_types.json()
                available_account_types = available_account_types["available account types"]


                # Form
                st.subheader("Please fill in the form below to create an account.")
                account_name = st.text_input(label="Account name")
                account_type = st.selectbox("Choose account type", available_account_types, key="account_type")
                account_balance = st.number_input("Balance", format="%.2f", key="balance_account_input")
                submit_button = st.form_submit_button(label='Create Account')

                # Request API when submit button is clicked
                if submit_button:
                    url = f"{api_url}/api/{api_version}/create/account?account_name={account_name}&account_type={account_type}&account_balance={account_balance}"
                    response = requests.post(url, headers=st.session_state.headers)
                    if response.status_code == 200:
                        st.success(response.json())
                    else:
                        st.error("An error occurred.")
                        st.write(response)


        # Delete account choice
        if create_delete_choice_account == "Delete Account":
            with st.form(key="delete_account_form"):

                # Get available accounts
                url = f"{api_url}/api/{api_version}/table/account"
                account_table = requests.get(url, headers=st.session_state.headers)
                account_table = account_table.json()
                account_table = account_table["account table"]

                if not account_table:
                    st.warning("No Account found")


                # Form
                st.subheader("Please choose an account to delete in the list below.")
                account_name_to_delete = st.selectbox("Choose account", [account[1] for account in account_table], key="account_name_delete")
                submit_button = st.form_submit_button(label='Delete Account')


                # Request API when submit button is clicked
                if submit_button:
                    account_id_to_delete = next((account[0] for account in account_table if account[1] == account_name_to_delete), None)
                    url = f"{api_url}/api/{api_version}/delete/account?account_id={account_id_to_delete}"
                    response = requests.delete(url, headers=st.session_state.headers)
                    if response.status_code == 200:
                        st.success(response.json())
                    else:
                        st.error("An error occurred.")
                        st.write(response)
                    


    # Budget Column
    with col_budget:
        # Button to choose : Create | Delete (budget)
        create_delete_choice_budget = st.radio("Choose", ["Create Budget", "Delete Budget"], key="create_delete_choice_budget")

        # Create budget choice
        if create_delete_choice_budget == "Create Budget":
            with st.form(key="create_budget_form"):

                # Form
                st.subheader("Please fill in the form below to create a budget.")
                budget_name = st.text_input(label="Budget name")
                budget_month = st.selectbox("Choose budget month", months, key="budget_month_create")
                budget_amount = st.number_input("Amount", format="%.2f", key="amount_budget_input")
                submit_button = st.form_submit_button(label='Create Budget')

                # Request API when submit button is clicked
                if submit_button:
                    url = f"{api_url}/api/{api_version}/create/budget?budget_name={budget_name}&budget_month={budget_month}&budget_amount={budget_amount}"
                    response = requests.post(url, headers=st.session_state.headers)
                    if response.status_code == 200:
                        st.success(response.json())
                    else:
                        st.error("An error occurred.")
                        st.write(response)


        # Delete budget choice
        if create_delete_choice_budget == "Delete Budget":
            with st.form(key="delete_budget_form"):

                # Get available budgets
                url = f"{api_url}/api/{api_version}/table/budget"
                budget_table = requests.get(url, headers=st.session_state.headers)
                budget_table = budget_table.json()
                budget_table = budget_table["budget table"]

                if not budget_table:
                    st.warning("No budget found")
                    st.stop()

                # Form
                st.subheader("Please choose an account to delete in the list below.")
                st.warning("This will delete all budget related transactions")
                budget_name_to_delete, budget_month_to_delete = st.selectbox("Choose budget", [(budget[1], budget[2]) for budget in budget_table], key="budget_name_delete")
                submit_button = st.form_submit_button(label='Delete Budget')


                # Request API when submit button is clicked
                if submit_button:

                    # Get budget id to delete
                    budget_id_to_delete = next((budget[0] for budget in budget_table if budget[1] == budget_name_to_delete), None)

                    # Get transactions id to delete
                    url = f"{api_url}/api/{api_version}/table/transaction"
                    transaction_table = requests.get(url, headers=st.session_state.headers)
                    transaction_table = transaction_table.json()
                    transaction_table = transaction_table["transaction table"]
                    transaction_id_related_budget = [transaction[0] for transaction in transaction_table if transaction[6] == budget_id_to_delete]           


                    # Delete all related transactions
                    for transaction_to_delete in transaction_id_related_budget:

                        url = f"{api_url}/api/{api_version}/delete/transaction?transaction_id={transaction_to_delete}"
                        response = requests.delete(url, headers=st.session_state.headers)
                        if response.status_code == 200:
                            st.success(response.json())
                        else:
                            st.error("An error occurred.")
                            st.write(response)                    


                    # Delete budget
                    url = f"{api_url}/api/{api_version}/delete/budget?budget_id={budget_id_to_delete}"
                    response = requests.delete(url, headers=st.session_state.headers)
                    if response.status_code == 200:
                        st.success(response.json())
                    else:
                        st.error("An error occurred.")
                        st.write(response)


### END OF PAGE: SETTINGS ###


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