"""
USE THIS SCRIPT TO GENERATE TEST OBJECTS FOR TESTING THE BANK APPLICATION (PYTEST)
"""
from __init__ import Account, Budget, Transaction

test_account_path = "./test_accounts.json"
test_budget_path = "./test_budgets.csv"
test_transaction_path = "./test_transactions.csv"



def generate_test_objects() -> None:

    test_origin_account = Account(name="test_origin_account", type="checking", amount=10000.0)
    test_origin_account.save(account_path = test_account_path)

    test_destination_account = Account(name="test_destination_account", type="checking", amount=10000.0)
    test_destination_account.save(account_path = test_account_path)

    test_budget = Budget(name="test_budget", month="June", amount=10000.0)
    test_budget.save(budget_path = test_budget_path)

    test_transaction = Transaction(type="debit", origin_account="test_origin_account", destination_account="test_destination_account", amount=10, budget="test_budget")
    test_transaction.save(transaction_path = test_transaction_path)


if __name__ == "__main__":
    generate_test_objects()
    print("Test objects generated successfully!")