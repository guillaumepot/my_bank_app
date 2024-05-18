"""
This file is used to run unit tests with Pytest
"""


"""
LIBS
"""
import pytest
import os
import pandas as pd
from datetime import datetime

from myBankPackage import Account, Budget, Transaction, generate_uuid, account_to_table, budget_to_table


"""
VARS
"""
# Path to the budget folder
budget_path = os.getenv("BUDGET_PATH", "./test_budgets/") 
# Path to the account folder
account_path = os.getenv("ACCOUNT_PATH", "./test_accounts/")
# Path to the transaction folder
transaction_path = os.getenv("TRANSACTION_PATH", "./test_transactions/test_transactions.csv")



"""
FIXTURES
"""
# Default account fixture
@pytest.fixture
def create_default_account() -> Account:
   """
   Create a default account as a fixture
   """
   default_account = Account(
      name="default_test_account",
      type="checking",
      amount=1000.0
   )
   return default_account


# Default budget fixture
@pytest.fixture
def create_default_budget() -> Budget:
   """
   Create a default budget as a fixture
   """
   default_budget = Budget(
      name="default_budget",
      month="June",
      amount=500.0
   )
   
   return default_budget


# Default transaction fixture
@pytest.fixture
def create_default_transaction() -> Transaction:
   """
   Create a default transaction as a fixture
   """
   default_transaction = Transaction(
        date=datetime.now(),
        type="credit",
        origin_account='origin_test',
        destination_account='destination_test',
        amount=50.0,
        budget='test budget',
        budget_month="June",
        description="Test transaction fixture")
   
   return default_transaction



"""
OBJECTS TESTS
"""
## ACCOUNT ##
@pytest.mark.parametrize("name, type, amount",
                         [
                             ("Test1", "checking", 1000),
                             ("Test2", "saving", 0.0),
                             ("Test3", "test", 100.0),
                             ("Test4", "checking", -50.0)
                             ])
def test_account_object(name, type, amount) -> None:
    """
    Test the Account object.
    """
    if name == "Test1":
        account = Account(name, type, amount)

        assert account.name == "Test1"
        assert account.type == "checking"
        assert account.amount == 1000.0

    # Saving Type
    elif name == "Test2":
        account = Account(name, type, amount)

        assert account.name == "Test2"
        assert account.type == "saving"
        assert account.amount == 0.0

    # Invalid type
    elif name == "Test3":
        with pytest.raises(TypeError):
            account = Account(name, type, amount)

    # Invalid amount
    elif name == "Test4":
        with pytest.raises(ValueError):
            account = Account(name, type, amount)


@pytest.mark.parametrize("test, deposit_amount, withdraw_amount",
                         [
                             (1, 500, 1000),
                             (2, 25.5, 5000)
                             ])
def test_account_deposit_and_withdraw(test, deposit_amount, withdraw_amount, create_default_account) -> None:
    """
    Test the deposit and withdraw methods of the Account object.
    """
    base_amount = create_default_account.amount

    if test == 1:
        # Deposit
        create_default_account.deposit(deposit_amount, "1")
        assert create_default_account.amount == base_amount + deposit_amount

        # Withdraw
        create_default_account.withdraw(withdraw_amount, "2")
        assert create_default_account.amount == base_amount + deposit_amount - withdraw_amount

    elif test == 2:
        # Deposit
        create_default_account.deposit(deposit_amount, "1")
        assert create_default_account.amount == base_amount + deposit_amount

        # Withdraw
        with pytest.raises(ValueError):
            create_default_account.withdraw(withdraw_amount, "2")


def test_account_history(create_default_account) -> None:
    """
    Test the history method of the Account object.
    """
    create_default_account.deposit(50, transaction_id = "1")
    create_default_account.withdraw(25, transaction_id = "2")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assert create_default_account.amount == 1025.0
    assert create_default_account.history == [
        {"date":date,
         "transaction_id":"1",
         "type":"deposit",
         "amount":50},
        {"date":date,
         "transaction_id":"2",
         "type":"withdraw",
         "amount":25}
        ]
    

def test_budget_save_method(create_default_budget) -> None:
    """
    Test the save method of the Budget object.
    """
    create_default_budget.save(budget_path)
    assert os.path.exists(budget_path)


def test_account_save_method(create_default_account) -> None:
    """
    Test the save method of the Account object.
    """
    create_default_account.save(account_path)
    assert os.path.exists(account_path)



## BUDGETS ##
@pytest.mark.parametrize("name, month, amount",[( "Test1", "June", 75.0),("Test2", "December", -50)])
def test_budget_object(name, month, amount) -> None:
    """
    Test the creation of a Budget object with the given name, month, and amount.
    """
    if name == "Test1":
        budget = Budget(
            name=name,
            month=month,
            amount=amount)
        
        assert budget.name == name
        assert budget.month == month
        assert budget.amount == amount

    elif name == "Test2":
        with pytest.raises(ValueError):
            budget = Budget(
                name=name,
                month=month,
                amount=amount)


def test_budget_deposit(create_default_budget, amount = 100.0) -> None:
    """
    Test the deposit method of the Budget object.
    """
    base_budget_amount = create_default_budget.amount
    create_default_budget.deposit(amount, transaction_id = "test_deposit_method")
    assert create_default_budget.amount == base_budget_amount + amount


@pytest.mark.parametrize("amount",[50.0, 600])
def test_budget_withdraw(create_default_budget, amount, transaction_id = "test_withdraw_mathod") -> None:
    """
    Test the withdraw method of the Budget object.
    """
    base_budget_amount = create_default_budget.amount
    if amount == 600.0:
        with pytest.raises(ValueError):
            create_default_budget.withdraw(amount, transaction_id)

    else:
        print(create_default_budget.amount, amount)
        create_default_budget.withdraw(amount, transaction_id)
        assert create_default_budget.amount == base_budget_amount - amount


def test_budget_save_method(create_default_budget) -> None:
    """
    Test the save method of the Budget object.
    """
    create_default_budget.save(budget_path)
    assert os.path.exists(budget_path)



## TRANSACTIONS ##
@pytest.mark.parametrize("test_nb, date, type, amount, budget, budget_month, origin_account, destination_account",
                         [
                             (1, None, "credit", 50.0, "test_budget", "January", None, "destination"),

                         ])
def test_transaction_object(test_nb, date, type, amount, budget, budget_month, origin_account, destination_account) -> None:
    """
    Test the Transaction object.
    """
    if test_nb == 1:
        transaction = Transaction(date=date, type=type, amount=amount, budget=budget, budget_month=budget_month, origin_account=origin_account, destination_account=destination_account)
        assert transaction.date == date
        assert transaction.type == type
        assert transaction.amount == amount
        assert transaction.budget == budget
        assert transaction.budget_month == budget_month
        assert transaction.origin_account == origin_account
        assert transaction.destination_account == destination_account


def test_transaction_save_method(create_default_transaction) -> None:
    """
    Test the save method of the Transaction object.
    """
    create_default_transaction.save(transaction_path = transaction_path)
    assert os.path.exists(transaction_path)


@pytest.mark.parametrize("date, type, amount, budget, budget_month, origin_account, destination_account",
                         [
                             (None, "debit", 50.0, "default_budget", "June", "default_test_account", None),
                             (None, "credit", 50.0, "default_budget", "June", None, "default_test_account"),
                             (None, "transfert", 50.0, None, None, "default_test_account", "default_test_account")
                             ])
def test_transaction_apply_method(date, type, amount, budget, budget_month, origin_account, destination_account) -> None:
    """
    Test the apply method of the Transaction object.
    """
    transaction = Transaction(date=date, type=type, amount=amount, budget=budget, budget_month=budget_month, origin_account=origin_account, destination_account=destination_account)
    transaction.apply(account_path = account_path, budget_path = budget_path)




"""
FUNCTION TESTS
"""
def test_generate_uuid() -> None:
    """
    Test the generate_uuid function.
    """
    uuid = generate_uuid()
    assert len(uuid) == 32
    assert isinstance(uuid, str)


def test_account_to_table() -> pd.DataFrame:
    """
    Test the account_to_table function.
    """
    account_table = account_to_table(account_path)
    assert isinstance(account_table, pd.DataFrame)


def test_budget_to_table() -> pd.DataFrame:
    """
    Test the budget_to_table function.
    """
    budget_table = budget_to_table(budget_path)
    assert isinstance(budget_table, pd.DataFrame)