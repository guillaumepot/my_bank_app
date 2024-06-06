




# Delete Account
@app.delete(f"/api/{api_version}/delete/account", name="delete_account", tags=['account'])
def app_delete_account(name: str, current_user: str = Depends(get_current_user)) -> dict:
    """
    Deletes a bank account with the specified name.

    Args:
        name (str): The name of the account to be deleted.
        current_user (str, optional): The current user. Defaults to Depends(get_current_user).

    Returns:
        dict: A dictionary containing a success message.

    """
    with engine.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM accounts
            WHERE name = :name
        """, {"name": name})

        conn.commit()

    return {"message": f"Account {name} deleted successfully."}


# Load Account Table
@app.get(f"/api/{api_version}/table/account", name="load_account_table", tags=['account'])
def app_load_account_table(current_user: str = Depends(get_current_user)) -> dict:
    """
    Load the account table from the database and return it as a JSON object.

    Parameters:
    - current_user (str): The username of the current user. Defaults to the result of the `get_current_user` function.

    Returns:
    - dict: A dictionary representing the account table in JSON format.

    """
    with engine.connect() as conn:
        result = conn.execute("SELECT * FROM accounts")
        accounts_table = pd.DataFrame(result.fetchall())

        if accounts_table.empty:
            return {"message": "No accounts found."}

        else:
            accounts_table_json = accounts_table.to_json()
            return accounts_table_json





""" 
Budget routes
"""
# Create Budget
@app.post(f"/api/{api_version}/create/budget", name="create_budget", tags=['budget'])
def app_create_budget(name: str,
                      month: str,
                      amount: float,
                      current_user: str = Depends(get_current_user)) -> dict:
    """
    Create a new budget for the specified month.

    Args:
        name (str): The name of the budget.
        month (str): The month for which the budget is created.
        amount (float): The amount allocated for the budget.
        current_user (str, optional): The current user. Defaults to Depends(get_current_user).

    Returns:
        dict: A dictionary containing a success message with the details of the created budget.

    Raises:
        HTTPException: If a budget with the same name already exists for the specified month.

    """
    with engine.connect() as conn:
        # Check if the budget name already exists for the current month
        result = conn.execute("SELECT name FROM budgets WHERE month = :month", {"month": month})
        budget_names = pd.DataFrame(result.fetchall(), columns=['name'])

        if name in budget_names['name'].values:
            raise HTTPException(status_code=400, detail="Budget already exists for this month")
        else:
            # Generate an id for the budget
            id = uuid.uuid4()
            history = {}

            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO accounts (id, name, month, amount, history)
                VALUES (%s, %s, %s, %s, %s)
            """, (id, name, month, amount, history))

            conn.commit()

    return {"message": f"Budget {name} created successfully. Month: {month}, Amount: {amount}"}


# Delete Budget
@app.delete(f"/api/{api_version}/delete/budget", name="delete_budget", tags=['budget'])
def app_delete_budget(name: str, month: str, current_user: str = Depends(get_current_user)) -> dict:
    """
    Deletes a budget from the accounts table.

    Args:
        name (str): The name of the budget.
        month (str): The month of the budget.
        current_user (str, optional): The current user. Defaults to Depends(get_current_user).

    Returns:
        dict: A dictionary containing a success message.
    """
    with engine.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM accounts
            WHERE name = :name AND month = :month
        """, {"name": name, "month": month})

        conn.commit()

    return {"message": f"Budget {name} deleted successfully."}


# Load Budget Table
@app.get(f"/api/{api_version}/table/budget", name="load_budget_table", tags=['budget'])
def app_load_budget_table(current_user: str = Depends(get_current_user)) -> dict:
    """
    Loads the budget table for the current user.

    Parameters:
    - current_user (str): The username of the current user.

    Returns:
    - budget_table (Table): The budget table for the current user.

    """
    with engine.connect() as conn:

        result = conn.execute("SELECT * FROM budgets")
        budgets_table = pd.DataFrame(result.fetchall())
        budgets_table_json = budgets_table.to_json()

    return budgets_table_json


# Get available budgets
@app.get(f"/api/{api_version}/get/budget", name="get_available_budgets", tags=['budget'])
def app_get_available_budgets(current_user: str = Depends(get_current_user)):
    """
    Get the list of available budgets for the current user.

    Parameters:
    - current_user (str): The username of the current user.

    Returns:
    - dict: A dictionary containing the list of available budgets.

    Example:
    {
        "available budgets": ["budget1", "budget2", "budget3"]
    }
    """
    available_budgets = []

    with engine.connect() as conn:
        result = conn.execute("SELECT name FROM budgets")
        budgets = pd.DataFrame(result.fetchall())
        available_budgets = budgets['name'].values

    return {"available budgets": available_budgets}





""" 
Transaction routes
"""
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