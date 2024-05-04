"""
PYTEST FILE FOR UNIT TESTING
"""
import sys
sys.path.append("src")
sys.path.append("storage")

import os
import pytest
from datetime import datetime


from objects import Account, Budget
from functions import generate_uuid, generate_transaction, apply_transaction

"""
VARS
"""
budget_path = os.getenv("BUDGET_PATH", "../storage/test_budgets.csv")
account_path = os.getenv("ACCOUNT_PATH", "../storage/test_accounts.json")


"""
GENERAL FUNCTIONS
"""
def test_generate_uuid() -> None:
    """
    Test the generate_uuid function.
    """
    uuid = generate_uuid()
    assert len(uuid) == 32




"""
TEST ACCOUNT OBJECT
"""
# Fixtures
@pytest.fixture
def create_default_account() -> Account:
   """
   Create a default account as a fixture
   """
   default_account = Account(
      name="default account",
      type="checking",
      amount=100.0
   )
   
   return default_account



@pytest.mark.parametrize("name, type, amount",[( "Test", "checking", 1000),("Test", "savings", 0.0)])
def test_account_creation(name, type, amount) -> None:
    """
    Test the creation of an Account object with the given name, type, and amount.

    Args:
        name (str): The name of the account.
        type (str): The type of the account.
        amount (float): The initial amount in the account.

    Returns:
        Account: The created Account object.

    Raises:
        AssertionError: If the created Account object does not have the expected attributes.

    """
    account = Account(
        name=name,
        type=type,
        amount=amount
    )
    assert account.name == name
    assert account.type == type
    assert account.amount == amount



def test_account_creation_with_invalid_type() -> None:
    """
    Test case to verify that an exception is raised when creating an account with an invalid type.
    """
    with pytest.raises(TypeError):
        account = Account(
            name="Test",
            type="invalid",
            amount=1000
        )



@pytest.mark.parametrize("amount", [1, 2.5])
def test_account_deposit(create_default_account, amount, transaction_id = "1") -> None :
    """
    Test the deposit method of the Account object.
    """
    create_default_account.deposit(amount, transaction_id)
    assert create_default_account.amount == 100 + amount



@pytest.mark.parametrize("amount", [25, -5, 101])
def test_account_withdraw(create_default_account, amount, transaction_id = "2") -> None:
    """
    Test the withdraw method of the Account object.
    """
    if amount < 0:
        with pytest.raises(ValueError):
            create_default_account.withdraw(amount, transaction_id)

    elif amount > create_default_account.amount:
        with pytest.raises(ValueError):
            create_default_account.withdraw(amount, transaction_id)

    else:
        create_default_account.withdraw(amount, transaction_id)
        assert create_default_account.amount == 100 - amount



def test_account_history(create_default_account) -> None:
    """
    Test the history method of the Account object.
    """
    create_default_account.deposit(50, transaction_id = "1")
    create_default_account.withdraw(25, transaction_id = "2")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assert create_default_account.amount == 125
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
    

"""
TEST BUDGET OBJECT
"""
# Fixtures
@pytest.fixture
def create_default_budget() -> Budget:
   """
   Create a default budget as a fixture
   """
   default_budget = Budget(
      name="default budget",
      month="June",
      amount=50.0
   )
   
   return default_budget


@pytest.mark.parametrize("name, month, amount",[( "Test", "June", 75.0),("Test", "July", 80.5)])
def test_budget_creation(name, month, amount) -> None:
    """
    Test the creation of a Budget object with the given name, month, and amount.
    """
    budget = Budget(
        name=name,
        month=month,
        amount=amount
    )
    assert budget.name == name
    assert budget.month == month
    assert budget.amount == amount



def test_add_amount(create_default_budget, amount = 100.0):
    """
    Test the add_amount method of the Budget object.
    """
    create_default_budget.add_amount(amount)
    assert create_default_budget.amount == 50.0 + amount



@pytest.mark.parametrize("amount",[50.0, 100.0])
def test_withdraw_amount(create_default_budget, amount, transaction_id = "1"):
    """
    Test the withdraw_amount method of the Budget object.
    """
    if amount == 100.0:
        with pytest.raises(ValueError):
            create_default_budget.withdraw_amount(amount, transaction_id)

    else:
        print(create_default_budget.amount, amount)
        create_default_budget.withdraw_amount(amount, transaction_id)
        assert create_default_budget.amount == 50.0 - amount


"""
TEST TRANSACTION FUNCTION
"""
@pytest.mark.parametrize("type, origin_account, destination_account, amount, budget",
                         [("debit", create_default_account, None, 50.0, None),
                          ("credit", None, create_default_account, 50.0, None),
                          ("transfert", create_default_account, create_default_account, 50.0, None)])
def test_generate_transaction(type,
                              origin_account,
                              destination_account,
                              amount,
                              budget) -> None:
    """
    Test the generate_transaction function.

    Args:
        type (str): The type of the transaction.
        origin_account (str): The origin account of the transaction.
        destination_account (str): The destination account of the transaction.
        amount (float): The amount of the transaction.
        budget (str): The budget of the transaction.

    Returns:
        None

    Raises:
        AssertionError: If any of the assertions fail.
    """
    date = None
    transaction = generate_transaction(date, type, origin_account, destination_account, amount, budget)
    assert transaction["type"] == type
    assert transaction["origin_account"] == origin_account
    assert transaction["destination_account"] == destination_account
    assert transaction["amount"] == amount
    assert transaction["budget"] == budget
    assert transaction["id"] != None



def test_apply_transaction(create_default_account) -> None:
    """
    Test the apply_transaction function.
    """
    transaction = generate_transaction(datetime.now(), "debit", create_default_account, None, 50.0, None)
    apply_transaction(transaction)
    assert create_default_account.amount == 100 - 50.0

    transaction = generate_transaction(datetime.now(), "credit", None, create_default_account, 50.0, None)
    apply_transaction(transaction)
    assert create_default_account.amount == 100