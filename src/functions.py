"""


"""


"""
LIBS
"""
import uuid
import os
import json
import pandas as pd
from datetime import datetime



"""
VARS
"""
budget_path = os.getenv("BUDGET_PATH", "../storage/test_budgets.csv")
account_path = os.getenv("ACCOUNT_PATH", "../storage/test_accounts.json")


"""
FUNCS
"""
def generate_uuid():
    return uuid.uuid4().hex


### LOADERS

def load_account_table(account_path:str) -> dict:
    """
    account_table = pd.read_json(account_path)
    return account_table.to_dict()
    """
    with open(account_path, "r") as file:
        account_table = json.load(file)
    return account_table



def load_specific_account(account_name: str, account_path: str = account_path) -> dict:
    """
    Load a specific account from the account table.

    Parameters:
    account_name (str): The name of the account to load.
    account_path (str, optional): The path to the account table file. Defaults to account_path.

    Returns:
    dict: The loaded specific account.

    Raises:
    ValueError: If the account is not found in the account table.
    """
    account_table = load_account_table(account_path)


    if account_name not in account_table:
        raise ValueError("Account not found")

    loaded_specific_account = account_table[account_name]

    return loaded_specific_account



def save_account_changes(account: dict, account_path: str = account_path) -> None:
    """
    Save the changes made to an account in the account table.

    Parameters:
    account (dict): The updated account to be saved.
    account_path (str, optional): The path to the account table file. Defaults to account_path.

    Returns:
    None
    """
    account_table = load_account_table(account_path)
    account_table[account['name']] = account
    with open(account_path, 'w') as file:
        json.dump(account_table, file, indent = 4)



def load_budget_table(budget_path:str):
    """
    Load the budget table from the budget file.

    Parameters:
    budget_path (str): The path to the budget file.

    Returns:
    pd.DataFrame: The loaded budget table.
    """
    budget_table = pd.read_csv(budget_path)
    budget_list = budget_table["name"].tolist()
    return budget_table, budget_list



def load_specific_budget(budget_name: str, budget_path: str = budget_path):
    """
    Load a specific budget from the budget table.

    Args:
        budget_name (str): The name of the budget to load.
        budget_path (str, optional): The path to the budget table file. Defaults to budget_path.

    Returns:
        pandas.DataFrame: The loaded budget as a pandas DataFrame.

    Raises:
        ValueError: If the specified budget is not found in the budget table.
    """
    budget_table, budget_list = load_budget_table(budget_path)

    # If budget not found, raise error
    if budget_name not in budget_list:
        raise ValueError("Budget not found")

    else:
        # Get current month
        month = datetime.now().strftime("%B")
        # Get budget according to name and month
        loaded_budget = budget_table[budget_table["name"] == "name" & budget_table["month"] == month]
        # Return
        return loaded_budget



def save_budget_change(loaded_budget, budget_name):
    """
    Save the changes made to a budget in the budget table.

    Parameters:
    loaded_budget (DataFrame): The updated budget to be saved.
    budget_name (str): The name of the budget to be updated.

    Returns:
    None

    Raises:
    None
    """
    # Load budget table
    budget_table = load_budget_table(budget_path)

    # Get current month
    month = datetime.now().strftime("%B")

    # Save
    budget_table[budget_table[budget_name] == budget_name & budget_table["month"] == month] = loaded_budget
    budget_table.to_csv(budget_path, index=False)




### TRANSACTIONS

def debit_transaction(transaction: dict, loaded_origin_account, loaded_budget) -> None:
    """
    Debits the specified amount from the origin account and updates the budget if provided.

    Args:
        transaction (dict): The transaction details, including the amount and budget (optional).
        loaded_origin_account: The origin account from which the amount will be debited.
        loaded_budget: The budget to be updated (optional).

    Raises:
        ValueError: If the origin account is not provided.

    Returns:
        None
    """
    # Check if origin account is provided
    if loaded_origin_account == None:
        raise ValueError("Origin account is required for debit transaction")
    
    # Withdraw amount from origin account
    loaded_origin_account["amount"] -= transaction["amount"]
    # Save
    save_account_changes(loaded_origin_account)

    # If budget, update budget
    if transaction["budget"] is not None:
        loaded_budget["amount"] -= transaction["amount"]
        # Save
        save_budget_change(loaded_budget, transaction["budget"])



def credit_transaction(transaction: dict, loaded_destination_account, loaded_budget) -> None:
    """
    Credit the specified amount to the destination account and update the budget if provided.

    Args:
        transaction (dict): A dictionary containing transaction details.
        loaded_destination_account: The destination account object.
        loaded_budget: The budget object.

    Raises:
        ValueError: If the destination account is not provided.

    Returns:
        None
    """
    # Check if destination account is provided
    if loaded_destination_account == None:
        raise ValueError("Destination account is required for debit transaction")
    
    # Withdraw amount from destination account
    loaded_destination_account["amount"] += transaction["amount"]
    # Save
    save_account_changes(loaded_destination_account)

    # If budget, update budget
    if transaction["budget"] is not None:
        loaded_budget["amount"] += transaction["amount"]
        # Save
        save_budget_change(loaded_budget, transaction["budget"])



def transfert_transaction(transaction: dict, loaded_origin_account, loaded_destination_account) -> None:
    """
    Perform a transfer transaction between two accounts.

    Args:
        transaction (dict): The transaction details, including the amount.
        loaded_origin_account: The origin account from which the amount will be debited.
        loaded_destination_account: The destination account to which the amount will be credited.

    Raises:
        ValueError: If the origin account or destination account is not provided.

    Returns:
        None
    """
    # Check if origin account is provided
    if loaded_origin_account == None:
        raise ValueError("Origin account is required for debit transaction")

    # Check if destination account is provided
    if loaded_destination_account == None:
        raise ValueError("Destination account is required for debit transaction")

    # Withdraw amount from origin account
    loaded_origin_account["amount "]-= transaction["amount"]
    # Save
    loaded_origin_account.save()

    # Withdraw amount from destination account
    loaded_destination_account["amount"] += transaction["amount"]

    # Save
    save_account_changes(loaded_origin_account)
    save_account_changes(loaded_destination_account)



def generate_transaction(date = None,
                         type:str="debit",
                         origin_account:str=None,
                         destination_account:str=None,
                         amount:float=0.0,
                         budget=None) -> None:
    """
    Generate a transaction with the given parameters.

    Parameters:
    - date (str, optional): The date of the transaction in the format "YYYY-MM-DD HH:MM:SS". If not provided, the current date and time will be used.
    - type (str, optional): The type of the transaction. Allowed values are "debit", "credit", and "transfert". Defaults to "debit".
    - origin_account (str, optional): The account from which the transaction originates. Defaults to None.
    - destination_account (str, optional): The account to which the transaction is sent. Defaults to None.
    - amount (float, optional): The amount of the transaction. Defaults to 0.0.
    - budget (optional): The budget associated with the transaction. Defaults to None.

    Returns:
    - transaction (dict): A dictionary representing the generated transaction with the following keys:
        - id (str): The unique identifier of the transaction.
        - date (str): The date of the transaction.
        - type (str): The type of the transaction.
        - origin_account (str): The account from which the transaction originates.
        - destination_account (str): The account to which the transaction is sent.
        - amount (float): The amount of the transaction.
        - budget: The budget associated with the transaction.
    """
    # Allowed transaction types
    allowed_types = ["debit", "credit", "transfert"]
    if type not in allowed_types:
        raise ValueError("Invalid transaction type")


    # Get current date if None
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    # Define transaction
    transaction = {
        "id": generate_uuid(),
        "date": date,
        "type": type,
        "origin_account": origin_account,
        "destination_account": destination_account,
        "amount": amount,
        "budget": budget
    }

    return transaction



def apply_transaction(transaction: dict) -> dict:
    """
    Apply a transaction to the specified accounts and budgets.

    Args:
        transaction (dict): A dictionary representing the transaction details.

    Returns:
        dict: The updated transaction dictionary.

    """
    ### LOAD ACCOUNTS AND BUDGETS

    # Load budget
    if transaction["budget"] is not None:
        # Load specified budget
        loaded_budget = load_specific_budget(budget_name = transaction["budget"])
    else:
        loaded_budget = None

    # Load origin account
    if transaction["origin_account"] is not None:
        loaded_origin_account = load_specific_account(transaction["origin_account"])
    else:
        loaded_origin_account = None

    # Load destination account
    if transaction["destination_account"] is not None:
        loaded_destination_account = load_specific_account(transaction["destination_account"])
    else:
        loaded_destination_account = None


    ### TRANSACTION TYPES

    # Debit
    if transaction["type"] == "debit":
        debit_transaction(transaction, loaded_origin_account, loaded_budget)

    # Credit
    elif transaction["type"] == "credit":
        credit_transaction(transaction, loaded_destination_account, loaded_budget)

    # Transfert
    else:
        transfert_transaction(transaction, loaded_origin_account, loaded_destination_account)


    # Return
    return transaction