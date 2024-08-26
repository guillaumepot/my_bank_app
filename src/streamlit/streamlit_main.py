"""
### STREAMLIT APP - Main file ###
"""

# LIBS
import calendar
import pandas as pd
import requests
import streamlit as st

from streamlit_api_requests_functions import api_version, api_url
from streamlit_api_requests_functions import get_api_status, validate_credentials, get_account_table, get_budget_table, get_transaction_table
from streamlit_api_requests_functions import post_transaction_creation, delete_transaction
from streamlit_api_requests_functions import get_bar_chart, get_time_series


# VARS
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
elt_to_display = ["All", "1", "5", "10", "15", "30", "50"]
login_data = {}


# STREAMLIT CONFIG
st.set_page_config(layout="wide") ### TEST ###


# API STATUS CHECKING
get_api_status()


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
if 'new_category' not in st.session_state:  # ADDED IN 0.2.1
    st.session_state.new_category = None


# Initialize session state for search and delete actions
if 'search_transaction_by_id_button_clicked' not in st.session_state:
    st.session_state.search_button_clicked = False
if 'transaction_id_to_remove' not in st.session_state:
    st.session_state.transaction_id_to_remove = None




### SIDEBAR ###

# Navigation
st.sidebar.title("Personal bank app")

# Authentication panel
st.sidebar.subheader("Authentication")
if st.session_state.access_token == None:

    # Display error message if not logged in on the main page
    st.error("Please Log In to access the app.")

    # Username & Password inputs
    login_username = st.sidebar.text_input("Username")
    login_password = st.sidebar.text_input("Password", type="password")

    # Define login_data
    login_data = {
        "grant_type": "",
        "username": login_username,
        "password": login_password,
        "scope": "",
        "client_id": "",
        "client_secret": ""
    }

    # Request API on submitted Log In button
    st.sidebar.button("Log In", on_click=validate_credentials, args=(login_data,))
    st.stop()


else:
    # Logout button
    st.sidebar.empty()
    if st.sidebar.button("Log Out", key="sidebar_logout_button"):
        st.session_state.pop('access_token', None)
        st.rerun()

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
    df_accounts = get_account_table()
    # Get budget table
    df_budgets, budget_id_to_name = get_budget_table()
    # Get transaction table
    df_transactions = get_transaction_table(budget_id_to_name)



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
        credit_amount = df_transactions[df_transactions["type"] == "credit"]["amount"].apply(lambda x: float(x.split(" ")[0])).sum()
        debit_amount = df_transactions[df_transactions["type"] == "debit"]["amount"].apply(lambda x: float(x.split(" ")[0])).sum()
        evaluated_amount = credit_amount - debit_amount
        st.markdown(f"**Evaluated amount in transactions:** {evaluated_amount:.2f} €", unsafe_allow_html=True)



### END OF PAGE: OVERVIEW ###




### TRANSACTIONS ###


# Transactions
if page == pages[1]: 
    st.title("Transactions")

    # Get transaction table
    df_budgets, budget_id_to_name = get_budget_table()
    df_transactions = get_transaction_table(budget_id_to_name)
    transaction_id_list = sorted(df_transactions.id.tolist())
    current_transaction_categories = [category for category in df_transactions["category"].unique()]
    current_transaction_categories.sort() # ADDED IN 0.2.1
    if st.session_state.new_category: # ADDED IN 0.2.1
        current_transaction_categories.insert(0, st.session_state.new_category) # CHANGED IN 0.2.1



    # Button to choose : Create | Delete (transaction)
    create_delete_choice_transaction = st.radio("Choose", ["Create Transaction", "Delete Transaction"], key="create_delete_choice_transaction")
    
    # Create transaction choice
    if create_delete_choice_transaction == "Create Transaction":
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
            account_names = [account['name'] for account in account_table]
            account_names.insert(0, "None")
    
            # Get available budgets
            url = f"{api_url}/api/{api_version}/table/budget"
            budget_table = requests.get(url, headers=st.session_state.headers)
            budget_table = budget_table.json()
            budget_table = budget_table["budget table"]
            budget_names = [budget['name'] for budget in budget_table]
            budget_names.insert(0, "None")
            budget_months = [budget['month'] for budget in budget_table]
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
            
            category = st.selectbox("Choose category", current_transaction_categories, key="transaction_category")
            # if category == "New Category":                        REMOVED SINCE 0.2.1
            #     category = st.text_input(label="New Category")    REMOVED SINCE 0.2.1

            description = st.text_input(label="Transaction Description")


            params = {
                "transaction_date": transaction_date.strip(),
                "transaction_type": transaction_type.strip(),
                "transaction_amount": transaction_amount,
                "origin_account": transaction_origin_account.strip(),
                "destination_account": transaction_destination_account.strip(),
                "budget_name": budget_name.strip(),
                "budget_month": budget_month.strip(),
                "recipient": transaction_recipient.strip(),
                "category": category.strip() if category is not None else "", # CHANGED IN 0.2.1
                "description": description.strip()
            }

            submit_button = st.form_submit_button(label='Create Transaction')


            # Request API when submit button is clicked
            if submit_button:
                post_transaction_creation(params)



    # Delete transaction choice
    if create_delete_choice_transaction == "Delete Transaction":

        with st.form(key="delete_transaction_form"):
            st.subheader("Select transaction id to remove:")
            transaction_id_to_remove = st.selectbox("Choose transaction id", transaction_id_list, key="transaction_id_choice")

            # Search button
            search_button = st.form_submit_button(label='Search')

            if search_button:
                st.session_state.search_transaction_by_id_button_clicked = True
                st.session_state.transaction_id_to_remove = transaction_id_to_remove

        if st.session_state.search_transaction_by_id_button_clicked:
            st.write("Delete this transaction ?")
            filtered_transaction_id = df_transactions[df_transactions["id"] == st.session_state.transaction_id_to_remove]
            st.dataframe(filtered_transaction_id)

            # Separate form for delete confirmation
            with st.form(key="confirm_delete_form"):
                submit_button = st.form_submit_button(label='Delete Transaction')

                # Request API when submit button is clicked
                if submit_button:
                    delete_transaction(st.session_state.transaction_id_to_remove)
                    st.success(f"Transaction {st.session_state.transaction_id_to_remove} has been deleted.")
                    # Reset session state
                    st.session_state.search_transaction_by_id_button_clicked = False
                    st.session_state.transaction_id_to_remove = None

### END OF PAGE: TRANSACTIONS ###


### ANALYTICS ###
if page == pages[2]: 
    st.title("Analytics")

    # Get transaction table
    df_budgets, budget_id_to_name = get_budget_table()
    df_transactions = get_transaction_table(budget_id_to_name)

    df_cat = df_transactions[["date", "type", "amount", "category", "recipient"]]
    df_cat["amount"] = df_cat["amount"].apply(lambda x: float(x.split(" ")[0])).astype(float) # Convert amount to float
    df_cat["year"] = pd.to_datetime(df_cat["date"]).dt.year.astype(str)
    df_cat["month"] = pd.to_datetime(df_cat["date"]).dt.month_name()
    df_cat["weekday"] = pd.to_datetime(df_cat["date"]).dt.weekday.apply(lambda x: calendar.day_name[x])
    df_time_series = df_cat.copy()

    # Build charts
    with st.expander("Bar plots"):

        plot_choice_col, transaction_type_col = st.columns(2)
        with plot_choice_col:
            plot_choice = st.selectbox("Plot choice:", ["Category", "Recipient", "Temporal"], key="plot_choice_analytics")
        with transaction_type_col:
            transaction_type = st.selectbox("Transaction type:", ["debit", "credit"], key="transaction_type_analytics")

            df_cat = df_cat[df_cat["type"] == transaction_type]

        if plot_choice == "Category" or plot_choice == "Recipient":
            temporal_choice = st.selectbox("Temporal choice:", ["", "Year", "Month", "Weekday"], key="temporal_choice_analytics")
            if temporal_choice == "Year":
                available_years_df_cat = [elt for elt in df_cat["year"].unique()]
                available_years_df_cat.insert(0, "")
                year_choice = st.selectbox("Choose year:", available_years_df_cat, key="year_choice_analytics")
                if year_choice != "":
                    df_cat = df_cat[df_cat["year"] == year_choice]

            if temporal_choice == "Month":
                available_months_df_cat = [elt for elt in df_cat["month"].unique()]
                available_months_df_cat.insert(0, "")
                month_choice = st.selectbox("Choose month:", available_months_df_cat, key="month_choice_analytics")
                if month_choice != "":
                    df_cat = df_cat[df_cat["month"] == month_choice]

            if temporal_choice == "Weekday":
                available_weekdays_df_cat = [elt for elt in df_cat["weekday"].unique()]
                available_weekdays_df_cat.insert(0, "")
                weekday_choice = st.selectbox("Choose weekday:", available_weekdays_df_cat, key="weekday_choice_analytics")
                if weekday_choice != "":
                    df_cat = df_cat[df_cat["weekday"] == weekday_choice]

        if plot_choice == "Category":
            df_cat = df_cat.groupby("category").agg({"amount": "sum"}).sort_values("amount", ascending=False).reset_index()
            get_bar_chart(df_cat, "category", "amount")

        elif plot_choice == "Recipient":
            df_cat = df_cat.groupby("recipient").agg({"amount": "sum"}).sort_values("amount", ascending=False).reset_index()
            get_bar_chart(df_cat, "recipient", "amount")

        elif plot_choice == "Temporal":
            display_by_temporal = st.selectbox("Display by:", ["", "Year", "Month", "Weekday"], key="display_by_temporal_analytics")
            if display_by_temporal == "Year":
                df_cat = df_cat.groupby(["year", "category"]).agg({"amount": "sum"}).sort_values("amount", ascending=False).reset_index()
                get_bar_chart(df_cat, "year", "amount", legend=df_cat["category"].unique())

            if display_by_temporal == "Month":
                df_cat = df_cat.groupby(["month", "category"]).agg({"amount": "sum"}).sort_values("amount", ascending=False).reset_index()
                get_bar_chart(df_cat, "month", "amount", legend=df_cat["category"].unique())

            if display_by_temporal == "Weekday":
                df_cat = df_cat.groupby(["weekday", "category"]).agg({"amount": "sum"}).sort_values("amount", ascending=False).reset_index()
                get_bar_chart(df_cat, "weekday", "amount", legend=df_cat["category"].unique())

    with st.expander("Time series"):
        get_time_series(df_time_series)

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
    col_account, col_budget, col_category = st.columns(3)



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



    # Category Column       # ADDED IN 0.2.1
    with col_category:
        with st.form(key="create_new_category"):
            st.subheader("Create a new category")
            new_cat = st.text_input("New category name")
            submit_button = st.form_submit_button(label='Create new category')
            if submit_button:
                st.session_state.new_category = new_cat
                st.success(f"New category {new_cat} has been added to the current session.")



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
        <p>LinkedIn: <a href="https://www.linkedin.com/in/062guillaumepot/" target="_blank">Click Here</a></p>
    </footer>
    """
    st.sidebar.markdown(footer, unsafe_allow_html=True)

addSidebarFooter()