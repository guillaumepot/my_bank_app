
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