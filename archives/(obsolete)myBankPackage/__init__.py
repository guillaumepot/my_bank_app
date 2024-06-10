# Version
__version__ = '0.1.0'

# /!\ This package is deprecated /!\
"""
LIBS
"""
import uuid
import os
import pickle
import pandas as pd
from datetime import datetime
from dataclasses import dataclass, field


"""
VALUE RESTRICTIONS
"""
available_account_types = ("checking", "saving")
available_transactions_types = ("debit", "credit", "transfert")


"""
COMMON FUNCTIONS
"""
def generate_uuid() -> str:
    """
    Generates a random UUID used for acocunt ID, transaction ID, etc.
    """
    return uuid.uuid4().hex


def load_account(account_path:str, account_name:str=None):
    """
    Load an account from a file.

    Args:
        account_path (str): The path to the directory where the account files are stored.
        account_name (str): The name of the account to load.

    Returns:
        The loaded account object.

    Raises:
        ValueError: If the account name is not provided.
        FileNotFoundError: If the account file is not found.
    """
    # Account name is required
    if account_name is None:
        raise ValueError("Account name is required.")
    
    # Load the account
    try:
        with open(f"{account_path}{account_name}.pkl", 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Account {account_name} not found.")
    

def load_budget(budget_path:str, budget_name:str=None, budget_month:str=None):
    """
    Load a budget from a file.

    Args:
        budget_path (str): The path to the directory where the budget files are stored.
        budget_name (str): The name of the budget.
        budget_month (str): The month of the budget.

    Returns:
        The loaded budget.

    Raises:
        ValueError: If budget_name or budget_month is None.
        FileNotFoundError: If the budget file is not found.

    """
    # Budget name and month are required
    if budget_name is None or budget_month is None:
        raise ValueError("Budget name and month are required.")
    
    # Load the budget
    try:
        with open(f"{budget_path}{budget_name}_{budget_month}.pkl", 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Budget {budget_name} for month {budget_month} not found.")


def account_to_table(account_path) -> pd.DataFrame:
    """
    Convert account data stored as pickle files in the given account_path directory into a pandas DataFrame.

    Parameters:
    account_path (str): The path to the directory containing the account data pickle files.

    Returns:
    pandas.DataFrame: A DataFrame containing the account data with columns: "name", "type", "amount", "id", "history".
    """

    # Create an empty list
    account_data = []

    # Loop through the files in the account_path directory
    for file in os.listdir(account_path):
        if file.endswith(".pkl"):
            account_name = file.rsplit('.', 1)[0]
            account = load_account(account_path, account_name)
            # Append the account data to the list
            account_data.append(account.__dict__)

    # Convert the list to a DataFrame
    account_table = pd.DataFrame(account_data)

    return account_table


def budget_to_table(budget_path) -> pd.DataFrame:
    """
    Convert budget files in a given directory to a pandas DataFrame.

    Parameters:
    budget_path (str): The path to the directory containing the budget files.

    Returns:
    pandas.DataFrame: A DataFrame containing the budget information from the files.

    """
    # Create an empty list
    budget_data = []

    # Loop through the files in the budget_path directory
    for file in os.listdir(budget_path):
        if file.endswith(".pkl"):
            budget_name = file.rsplit('_', 1)[0]
            budget_month = file.rsplit('_', 1)[1].rsplit('.', 1)[0]
            budget = load_budget(budget_path, budget_name, budget_month)
            # Append the budget data to the list
            budget_data.append(budget.__dict__)

    # Convert the list to a DataFrame
    budget_table = pd.DataFrame(budget_data)

    return budget_table




"""
ACCOUNT
"""
### Account Dataclass ###
@dataclass(frozen=False, order=False)
class Account:
    """
    Represents a bank account.

    Attributes:
        name (str): The name of the account.
        type (str): The type of the account (checking or savings).
        amount (float): The amount of money in the account.
        id (str): The unique identifier of the account.
        history (list): The transaction history of the account.

    Methods:
        deposit(amount: float, transaction_id: str) -> None: Deposits the specified amount into the account.
        withdraw(amount: float, transaction_id: str) -> None: Withdraws the specified amount from the account.
        save(account_path: str) -> None: Saves the account to a file.
    """

    ### INIT ###
    # Name of the account
    name:str
    # Type of the account (checking or savings)
    type:str = "checking"
    # Amount of the account
    amount:float = 0.0


    ### NO INIT ###
    # Random ID is generated by a function
    id: str = field(init=False, default_factory=generate_uuid)
    # History
    history: list = field(init=False, default_factory=list)


    def __post_init__(self) -> None:
        # Check if the type is an instance of available_account_types
        if self.type not in available_account_types:
            raise TypeError(f"Invalid Account Type: {self.type}")
        # Check if the amount is a float and positive
        if self.amount < 0:
            raise ValueError(f"Invalid Account Amount: {self.amount}")
        


    def deposit(self, amount:float, transaction_id:str) -> None:
        """
        Deposits the specified amount into the account.

        Args:
            amount (float): The amount to deposit.
            transaction_id (str): The ID of the transaction.

        Raises:
            ValueError: If the amount is negative.

        """
        if amount < 0:
            raise ValueError(f"Invalid Deposit Amount: {amount}")
        self.amount += amount

        self.history.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "transaction_id": transaction_id,
            "type": "deposit",
            "amount": amount,
        })



    def withdraw(self, amount:float, transaction_id:str) -> None:
        """
        Withdraws the specified amount from the account.

        Args:
            amount (float): The amount to withdraw.
            transaction_id (str): The ID of the transaction.

        Raises:
            ValueError: If the amount is negative or if there are insufficient funds.

        """
        if amount < 0:
            raise ValueError(f"Invalid Withdraw Amount: {amount}")
        if amount > self.amount:
            raise ValueError(f"Insufficient funds to withdraw {amount} from account {self.name}.")
        
        
        self.amount -= amount

        self.history.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "transaction_id": transaction_id,
            "type": "withdraw",
            "amount": amount,
        })



    def save(self, account_path:str) -> None:
        """
        Saves the account to a file.

        Args:
            account_path (str): The path where the account file will be saved.

        """
        # Check if account already exists
        if os.path.exists(f"{account_path}{self.name}.pkl"):
            print (f"Existing account {self.name} will be overwritten.")
        # Save the account
        with open(f"{account_path}{self.name}.pkl", 'wb') as f:
            pickle.dump(self, f)


"""
BUDGET
"""
### Budget Dataclass ###
@dataclass(frozen=False, order=False)
class Budget:
    """
    Represents a budget for a specific month.

    Attributes:
        name (str): The name of the budget.
        month (str): The month of the budget.
        amount (float): The amount of money allocated for the budget.

    Methods:
        deposit(amount: float, transaction_id: str) -> None: Deposits the specified amount of money into the budget.
        withdraw(amount: float, transaction_id: str) -> None: Withdraws the specified amount of money from the budget.
        save(budget_path: str) -> None: Saves the budget to a file.

    """

    ### INIT ###
    name: str
    month: str
    amount: float = 0.0


    ### NO INIT ###
    # Random ID is generated by a function
    id: str = field(init=False, default_factory=generate_uuid)
    # History
    history: list = field(init=False, default_factory=list)


    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError(f"Invalid Budget Amount (negative value): {self.amount}")


    def deposit(self, amount: float, transaction_id:str) -> None:
        """
        Deposits the specified amount of money into the budget.

        Args:
            amount (float): The amount of money to deposit.
            transaction_id (str): The ID of the transaction.

        Returns:
            None

        """
        self.amount += amount
        self.history.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "transaction_id": transaction_id,
            "amount": amount
        })


    def withdraw(self, amount: float, transaction_id: str) -> None:
        """
        Withdraws the specified amount of money from the budget.

        Args:
            amount (float): The amount of money to withdraw.
            transaction_id (str): The ID of the transaction.

        Returns:
            None

        Raises:
            ValueError: If the specified amount is greater than the current amount in the budget.

        """
        if amount > self.amount:
            raise ValueError(f"Not enough money in budget. Current amount: {self.amount}")

        self.amount -= amount
        self.history.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "transaction_id": transaction_id,
            "amount": amount
        })


    def save(self, budget_path: str) -> None:
        """
        Saves the budget to a file.

        Args:
            budget_path (str): The path where the budget file will be saved.

        Returns:
            None

        """
        # Check if budget already exists
        if os.path.exists(f"{budget_path}{self.name}.pkl"):
            print (f"Existing budget {self.name} will be overwritten.")
        # Save the budget
        with open(f"{budget_path}{self.name}_{self.month}.pkl", 'wb') as f:
            pickle.dump(self, f)



"""
TRANSACTION
"""
### Transaction Dataclass ###
@dataclass(frozen=False, order=False)
class Transaction:
    """
    Represents a financial transaction.

    Attributes:
        id (str): The unique identifier of the transaction.
        date (str): The date of the transaction in the format "YYYY-MM-DD".
        type (str): The type of the transaction (debit, credit, or transfert).
        amount (float): The amount of the transaction.
        origin_account (str): The origin account of the transaction.
        destination_account (str): The destination account of the transaction.
        budget (str): The budget associated with the transaction.
        budget_month (str): The month of the budget associated with the transaction.
        description (str): Additional description for the transaction.

    Methods:
        __post_init__(): Performs validation checks after the object is initialized.
        save(transaction_path: str): Saves the transaction to a CSV file.
        apply(account_path: str, budget_path: str): Applies the transaction to the accounts and budgets.
    """
    ### NO INIT ###

    # Random ID is generated by a function
    id: str = field(init=False, default_factory=generate_uuid)


    ### INIT ###
    date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    type:str = "debit"
    amount:float = 0.0
    origin_account:str = None
    destination_account:str = None
    budget:str = None
    budget_month:str = None
    description:str=""


    def __post_init__(self) -> None:
        """
        Performs validation checks after the object is initialized.
        Raises:
            TypeError: If the transaction type is invalid.
            ValueError: If the amount is negative, or if required fields are missing.
        """
        # Check if the type is an instance of available_account_types
        if self.type not in available_transactions_types:
            raise TypeError(f"Invalid Transaction Type: {self.type}")
        # Check if the amount is a float and positive
        if self.amount < 0:
            raise ValueError(f"Invalid Account Amount: {self.amount}")
        # If budget, check if it exists
        if (self.budget is not None) and (self.budget_month is None):
            raise ValueError("Budget month is required when budget is not None.")
        # If type is credit, destination account is required
        if (self.type == "credit") and (self.destination_account is None):
            raise ValueError("Destination account is required for credit transactions.")
        # If type is debit, origin account is required
        if (self.type == "debit") and (self.origin_account is None):
            raise ValueError("Origin account is required for debit transactions.")
        # If type is transfert, both origin and destination accounts are required
        if (self.type == "transfert") and ((self.origin_account is None) or (self.destination_account is None)):
            raise ValueError("Origin and destination accounts are required for transfert transactions.")
        

    def save(self, transaction_path:str) -> None:
        """
        Saves the transaction to a CSV file.

        Args:
            transaction_path (str): The path to the CSV file.

        Raises:
            FileNotFoundError: If the specified file path does not exist.
        """
        if os.path.exists(transaction_path) and os.path.getsize(transaction_path) > 0:
            transaction_table = pd.read_csv(transaction_path)
        else:
            transaction_table = pd.DataFrame(columns=self.__dict__.keys())
            
        # Save the transaction to the CSV file
        new_transaction_row = pd.Series(self.__dict__)
        transaction_table = pd.concat([transaction_table, new_transaction_row.to_frame().T], ignore_index=True)
        transaction_table.to_csv(transaction_path, index=False)


    def apply(self, account_path:str, budget_path:str) -> None:
        """
        Applies the transaction to the accounts and budgets.

        Args:
            account_path (str): The path to the accounts file.
            budget_path (str): The path to the budgets file.

        Raises:
            FileNotFoundError: If the specified file paths do not exist.
        """
        ## Load accounts & budgets
        # Load origin_account
        if self.origin_account is not None:
            loaded_origin_account = load_account(account_path, self.origin_account)

        # Load destination_account
        if self.destination_account is not None:
            loaded_destination_account = load_account(account_path, self.destination_account)


        # Load budget
        if self.budget is not None:
            loaded_budget = load_budget(budget_path=budget_path, budget_name=self.budget, budget_month=self.budget_month)


        ## Apply transaction
        # Debit
        if self.type == "debit":
            # Update amount
            loaded_origin_account.withdraw(self.amount, self.id)
            # Save changes
            loaded_origin_account.save(account_path)
            # Update budget
            if self.budget is not None:
                loaded_budget.withdraw(self.amount, self.id)
                loaded_budget.save(budget_path)


        # Credit
        elif self.type == "credit":
            # Update amount
            loaded_destination_account.deposit(self.amount, self.id)
            # Save changes
            loaded_destination_account.save(account_path)
            # Update budget
            if self.budget is not None:
                loaded_budget.deposit(self.amount, self.id)
                loaded_budget.save(budget_path)

        # Transfert
        else:
            # Update origin account
            loaded_origin_account.withdraw(self.amount, self.id)
            loaded_origin_account.save(account_path)
            # Update destination account
            loaded_destination_account.deposit(self.amount, self.id)
            loaded_destination_account.save(account_path)

if __name__ == "__main__":
    pass