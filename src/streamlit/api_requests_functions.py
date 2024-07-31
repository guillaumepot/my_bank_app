import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import os
import pandas as pd
import requests
import streamlit as st


# API VARS
api_version = os.getenv("API_VERSION", "0.1.4")
api_url = os.getenv("API_URL", "http://localhost:8000")

login_placeholder = st.sidebar.empty()



def get_api_status() -> None:
    """
    Request the api to get the status, block app if API is not responsding (or bad version)
    """
    url = f"{api_url}/api/{api_version}/status"
    response = requests.get(url)
    if response.status_code != 200:
        st.error("Error while checking API status.")
        st.stop()


def validate_credentials(login_data: dict) -> None:
    """
    This function will be called when the "Log In" button is pressed
    """
    # Request API
    url = f"{api_url}/api/{api_version}/login"
    response = requests.post(url, data=login_data)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        login_placeholder.empty()
        st.session_state.access_token = access_token
        st.sidebar.empty()

    else:
        st.sidebar.error("Incorrect Username or Password.")
  

def get_account_table() -> pd.DataFrame:
    """
    Retrieves the account table from the API and returns it as a pandas DataFrame.

    Returns:
        pd.DataFrame: The account table with columns: "name", "type", "balance", and "created_at".
    """
    # Request API
    url = f"{api_url}/api/{api_version}/table/account"
    account_table = requests.get(url, headers=st.session_state.headers)
    account_table = dict(account_table.json())
    account_table = account_table['account table']

    # Generate DF
    df_accounts = pd.DataFrame(account_table, columns=["id", "name", "type", "balance", "owner_id", "created_at"])
    df_accounts["balance"] = df_accounts["balance"].apply(lambda x: f"{x:.2f} €")
    df_accounts.drop(columns=["id", "owner_id"], inplace=True)
    df_accounts["created_at"] = df_accounts["created_at"].str.split("T").str[0]

    return df_accounts


def get_budget_table() -> pd.DataFrame:
    """
    Retrieves the budget table from the API and returns it as a pandas DataFrame.

    Returns:
        df_budgets (pd.DataFrame): The budget table as a pandas DataFrame.
        budget_id_to_name (dict): A dictionary mapping budget IDs to budget names.
    """
    # Request API
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

    return df_budgets, budget_id_to_name


def get_transaction_table(budget_id_to_name) -> pd.DataFrame:
    """
    Retrieves the transaction table from the API and returns it as a pandas DataFrame.

    Parameters:
    - budget_id_to_name (dict): A dictionary mapping budget IDs to their corresponding names.

    Returns:
    - df_transactions (pd.DataFrame): The transaction table as a pandas DataFrame, with columns for date, type, amount, origin account, destination account, budget, recipient, category, and description.
    """

    # Request API
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

    return df_transactions



def post_transaction_creation(transaction_data: dict) -> None:
    """
    Sends a POST request to create a new transaction.

    Args:
        transaction_data (dict): A dictionary containing the transaction data.

    Returns:
        None

    Raises:
        None

    """
    url = f"{api_url}/api/{api_version}/create/transaction"

    response = requests.post(url, params=transaction_data, headers=st.session_state.headers)
    if response.status_code == 200:
        st.success(response.json())
    else:
        st.error("An error occurred.")


def delete_transaction(transaction_id_to_remove: str) -> None:
    """
    Deletes a transaction with the specified transaction ID.

    Parameters:
        transaction_id_to_remove (str): The ID of the transaction to be deleted.

    Returns:
        None

    Raises:
        None
    """
    url = f"{api_url}/api/{api_version}/delete/transaction?transaction_id={transaction_id_to_remove}"
    response = requests.delete(url, headers=st.session_state.headers)
    if response.status_code == 200:
        st.success(response.json())
    else:
        st.error("An error occurred.")
        st.write(response)



def get_bar_chart(df, name, amount, legend=None):
    """
    Generate a bar chart based on the given DataFrame.

    Parameters:
    - df (pandas.DataFrame): The DataFrame containing the data for the chart.
    - name (str): The name of the column to be used as the x-axis.
    - amount (str): The name of the column to be used as the y-axis.
    - legend (list, optional): A list of labels for the legend. Default is None.

    Returns:
    None
    """
    x = df[name]
    y = df[amount]
    fig = plt.figure(figsize=(10, 5))
    colors = cm.viridis(np.linspace(0, 1, len(x)))

    bars = plt.bar(x, y, color=colors)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height - (height*0.05), f'{height}'+"€", ha='center', va='top', color='white') 

    plt.title(f"{name} expenses")
    plt.xlabel(name, fontweight='bold', rotation = 90)
    plt.ylabel(amount, fontweight='bold')

    if legend is not None:
        labels = [elt for elt in legend]
        plt.legend(bars, labels, title="Categories")

    st.pyplot(fig)


def get_time_series(df):
    """
    Calculate the cumulative sum of expenses over time and plot the results.
    
    Parameters:
    - df (pandas.DataFrame): The input DataFrame containing the expenses data.
    
    Returns:
    None
    """
    # Convert 'date' to datetime format
    df['date'] = pd.to_datetime(df['date'])
    
    df['year_month'] = df['date'].dt.to_period('M')
    df = df.groupby('year_month')['amount'].sum().reset_index()
    
    # Calculate cumulative sum
    df["cumsum"] = df["amount"].cumsum()

    # Plot
    fig = plt.figure(figsize=(10, 5))
    plt.plot(df['year_month'].astype(str), df["cumsum"], color="blue")  # Convert 'year_month' to string for plotting
    plt.fill_between(df['year_month'].astype(str), df["cumsum"], color="blue", alpha=0.3)
    plt.title("Cumulative expenses over time")
    plt.xlabel("Date", fontweight='bold', rotation=90)
    plt.ylabel("Amount", fontweight='bold')
    st.pyplot(fig)