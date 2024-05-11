"""
This file is used to run unit tests with Pytest
"""


"""
LIBS
"""
import pytest
from datetime import datetime

from myBankPackage import Account, Budget, Transaction, generate_uuid


"""
VARS
"""
test_account_path = "./test_accounts.json"
test_budget_path = "./test_budgets.csv"
test_transaction_path = "./test_transactions.csv"




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
      name="default test account",
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
      name="default budget",
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
        description="Test transaction fixture")
   
   return default_transaction



"""
OBJECTS TESTS
"""
## ACCOUNT ##
@pytest.mark.parametrize("name, type, amount",
                         [
                             ("Test1", "checking", 1000),
                             ("Test2", "savings", 0.0),
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
        assert account.type == "savings"
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
def test_budget_withdraw_amount(create_default_budget, amount, transaction_id = "test_withdraw_mathod") -> None:
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



## TRANSACTIONS ##
@pytest.mark.parametrize("test_nb, date, type, amount, budget, origin_account, destination_account",
                         [
                             (1, datetime.now(), "debit", 50.0, "Food", "origin", None),
                             (2, None, "credit", 50.0, "Fuel", None, "destination"),
                             (3, None, "transfert", 50.0, None, "origin_account", "destination_account"),
                             (4, None, "test", 50.0, "Food", "origin", None),
                             (5, None, "debit", -50.0, "Food", "origin", None),
                         ])
def test_transaction_object(test_nb, date, type, amount, budget, origin_account, destination_account) -> None:
    """
    Test the Transaction object.
    """
    if test_nb == 1:
        transaction = Transaction(date=date, type=type, amount=amount, budget=budget, origin_account=origin_account, destination_account=destination_account)
        assert transaction.date == date
        assert transaction.type == type
        assert transaction.amount == amount
        assert transaction.budget == budget
        assert transaction.origin_account == origin_account
        assert transaction.destination_account == destination_account

    elif test_nb == 2:
        transaction = Transaction(date=date, type=type, amount=amount, budget=budget, origin_account=origin_account, destination_account=destination_account)
        assert transaction.date == date
        assert transaction.type == type
        assert transaction.amount == amount
        assert transaction.budget == budget
        assert transaction.origin_account == origin_account
        assert transaction.destination_account == destination_account

    elif test_nb == 3:
        transaction = Transaction(date=date, type=type, amount=amount, budget=budget, origin_account=origin_account, destination_account=destination_account)
        assert transaction.date == date
        assert transaction.type == type
        assert transaction.amount == amount
        assert transaction.budget == budget
        assert transaction.origin_account == origin_account
        assert transaction.destination_account == destination_account

    elif test_nb == 4:
        with pytest.raises(TypeError):
            transaction = Transaction(date=date, type=type, amount=amount, budget=budget, origin_account=origin_account, destination_account=destination_account)

    elif test_nb == 5:
        with pytest.raises(ValueError):
            transaction = Transaction(date=date, type=type, amount=amount, budget=budget, origin_account=origin_account, destination_account=destination_account)
    

@pytest.mark.parametrize("date, type, amount, budget, origin_account, destination_account",
                         [
                             (datetime.now(), "debit", 50.0, "Test Budget", "test_origin_account", None),
                             (None, "credit", 50.0, "Test Budget", None, "test_destination_account"),
                             (None, "transfert", 50.0, None, "test_origin_account", "test_destination_account")
                             ])
def test_transaction_apply_method(date, type, amount, budget, origin_account, destination_account) -> None:
    """
    Test the apply method of the Transaction object.
    """
    transaction = Transaction(date=date, type=type, amount=amount, budget=budget, origin_account=origin_account, destination_account=destination_account)
    transaction.apply_transaction(account_path = test_account_path, budget_path = test_budget_path)




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