import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import os
import pandas as pd
import requests
import streamlit as st


# API VARS
api_version = os.getenv("API_VERSION", "0.1.2")
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



def get_bar_chart(df, name, amount, legend=None):
    """
    
    """
    x = df[name]
    y = df[amount]
    fig = plt.figure(figsize=(10, 5))
    colors = cm.viridis(np.linspace(0, 1, len(x)))

    bars = plt.bar(x, y, color=colors)

    #if legend is None:
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height - (height*0.05), f'{height}'+"€", ha='center', va='top', color='white') 

    plt.title(f"{name} expenses")
    plt.xlabel(name, fontweight='bold')
    plt.ylabel(amount, fontweight='bold')

    if legend is not None:
        labels = [elt for elt in legend]
        plt.legend(bars, labels, title="Categories")

    st.pyplot(fig)


def get_time_series(df):
    """
    
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
    plt.xlabel("Date", fontweight='bold')
    plt.ylabel("Amount", fontweight='bold')
    st.pyplot(fig)