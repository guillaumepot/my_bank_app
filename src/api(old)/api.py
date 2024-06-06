
# Create Transaction
@app.post(f"/api/{api_version}/create/transaction", name="create_transaction", tags=['transaction'])
def app_create_transaction(date:str,
                           type:str,
                           amount:float,
                           origin_account:str=None,
                           destination_account:str=None,
                           budget:str=None,
                           budget_month:str=None,
                           category:str="",
                           description:str="",
                           current_user: str = Depends(get_current_user)) -> dict:
    """
    Create a transaction in the bank application.

    Parameters:
    - date (str): The date of the transaction.
    - type (str): The type of the transaction (debit, credit, transfer).
    - amount (float): The amount of the transaction.
    - origin_account (str, optional): The name of the origin account for debit or transfer transactions.
    - destination_account (str, optional): The name of the destination account for credit or transfer transactions.
    - budget (str, optional): The name of the budget for the transaction.
    - budget_month (str, optional): The month of the budget for the transaction.
    - category (str, optional): The category of the transaction.
    - description (str, optional): The description of the transaction.
    - current_user (str, optional): The current user making the transaction.

    Returns:
    - dict: A dictionary containing the message indicating the success of the transaction creation and application.

    Raises:
    - HTTPException: If the transaction type is debit and the origin account is not provided.
    - HTTPException: If the transaction type is credit and the destination account is not provided.
    - HTTPException: If the transaction type is transfer and either the origin or destination account is not provided.
    """

    # Check if the transaction is valid
    if type not in available_transactions_types:
        raise HTTPException(status_code=400, detail="Invalid transaction type.")
    if type == "debit" and origin_account is None:
        raise HTTPException(status_code=400, detail="Origin account is required for debit transactions.")
    if type == "credit" and destination_account is None:
        raise HTTPException(status_code=400, detail="Destination account is required for credit transactions.")
    if type == "transfer" and (origin_account is None or destination_account is None):
        raise HTTPException(status_code=400, detail="Origin and destination accounts are required for transfer transactions.")


    # Create the transaction
    with engine.connect() as conn:
        id = uuid.uuid4()

        if budget == None:
            budget_id = 0
            budget_month = "N/A"

        result = conn.execute("SELECT id FROM users WHERE username = :username", {"username": current_user})
        budget_id = pd.DataFrame(result.fetchall(), columns=['id'])['id'].values[0]


        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (id, date, type, amount, origin_account, destination_account, budget, category, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (id, date, type, amount, origin_account, destination_account, budget_id, category, description))

        conn.commit()


    # Apply the transaction to the accounts and budgets
    with engine.connect() as conn:
        cursor = conn.cursor()

    if type == "debit":
        cursor.execute("""
            UPDATE accounts
            SET balance = balance - :amount,
                history = history || jsonb_build_object('transaction', :id)
            WHERE name = :origin_account
        """, {"amount": amount, "origin_account": origin_account, "id": str(id)})

    if type == "credit":
        cursor.execute("""
            UPDATE accounts
            SET balance = balance + :amount,
                history = history || jsonb_build_object('transaction', :id)
            WHERE name = :destination_account
        """, {"amount": amount, "destination_account": destination_account, "id": str(id)})

    if type == "transfer":
        cursor.execute("""
            UPDATE accounts
            SET balance = balance - :amount,
                history = history || jsonb_build_object('transaction', :id)
            WHERE name = :origin_account
        """, {"amount": amount, "origin_account": origin_account, "id": str(id)})

        cursor.execute("""
            UPDATE accounts
            SET balance = balance + :amount,
                history = history || jsonb_build_object('transaction', :id)
            WHERE name = :destination_account
        """, {"amount": amount, "destination_account": destination_account, "id": str(id)})

    if budget != None:
        cursor.execute("""
            UPDATE budgets
            SET amount = amount - :amount,
                history = history || jsonb_build_object('transaction', :id)
            WHERE name = :budget AND month = :month
        """, {"amount": amount, "budget": budget, "month": budget_month, "id": str(id)})


    conn.commit()


    return {"message": "Transaction created & applied successfully."}


# Get available transaction types
@app.get(f"/api/{api_version}/available/transaction_types", name="get_available_transaction_types", tags=['transaction'])
def app_get_available_transaction_types(current_user: str = Depends(get_current_user)):
    """
    Retrieves the available transaction types for the current user.

    Parameters:
    - current_user (str): The username of the current user.

    Returns:
    - available_transactions_types (list): A list of available transaction types.

    """
    return available_transactions_types


# Load Transaction Table
@app.get(f"/api/{api_version}/table/transaction", name="load_transaction_table", tags=['transaction'])
def app_load_transaction_table(current_user: str = Depends(get_current_user)):
    """
    Load the transaction table from the database and return it as a JSON string.

    Parameters:
    - current_user (str): The username of the current user.

    Returns:
    - str: A JSON string representing the transaction table.

    Raises:
    - None

    Example Usage:
    >>> app_load_transaction_table("john_doe")
    '{"transaction_id": [1, 2, 3], "amount": [100, 200, 300], ...}'
    """
    with engine.connect() as conn:
        result = conn.execute("SELECT * FROM transactions")
        transactions_table = pd.DataFrame(result.fetchall())
        transactions_table_json = transactions_table.to_json()

    return transactions_table_json