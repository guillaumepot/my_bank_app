"""
PostGres Database connectors for the API
"""


"""
LIBS
"""
import os
import psycopg2
from psycopg2.extras import DictCursor


"""
VARS
"""


postgres_host = os.getenv('POSTGRES_HOST', 'localhost')
postgres_port = os.getenv('POSTGRES_PORT', 5432)
postgres_user = os.getenv('POSTGRES_USER', 'root')
postgres_password = os.getenv('POSTGRES_PASSWORD', 'root')
postgres_db = os.getenv('POSTGRES_DB', 'bank_db')


"""
FUCNTIONS
"""
def connect_to_db() -> psycopg2.extensions.connection:
    """
    Connects to the database using the provided credentials.

    Returns:
        psycopg2.extensions.connection: A connection object representing the database connection.
    """
    engine = psycopg2.connect(dbname=postgres_db,
                            user=postgres_user,
                            password=postgres_password,
                            host=postgres_host,
                            port=postgres_port)
    
    return engine


def transform_additional(additional):
    """
    Transforms the additional parameter into a tuple if it is a string.

    Args:
        additional (str or tuple): The additional parameter to be transformed.

    Returns:
        tuple: The transformed additional parameter.

    """
    if isinstance(additional, str):
        return (additional,)
    else:
        return additional


def query_for_informations(request_to_do: str = None, additional=None) -> dict:
    """
    Execute a database query based on the given request and additional parameters.

    Args:
        request_to_do (str): The type of request to execute. Possible values are:
            - 'get_username_informations': Retrieve user information based on the username.
            - 'get_existing_accounts': Retrieve all existing accounts.
            - 'get_existing_budgets': Retrieve all existing budgets.
            - 'get_existing_transactions': Retrieve all existing transactions.
        additional: Additional parameters to be used in the query.

    Returns:
        dict: A dictionary containing the results of the query.

    Raises:
        psycopg2.OperationalError: If there is an error executing the query or connecting to the database.
    """
    additional = transform_additional(additional)

    # Initialize query
    if request_to_do == 'get_username_informations':
        query = "SELECT * FROM users WHERE username=%s"

    if request_to_do == 'get_existing_accounts':
        query = 'SELECT * FROM accounts'

    if request_to_do == 'get_existing_budgets':
        query = 'SELECT * FROM budgets'

    if request_to_do == 'get_existing_transactions':
        query = 'SELECT * FROM transactions'

    # Get engine
    engine = connect_to_db()

    # Apply Query
    with engine as conn:
        try:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                try:
                    cur.execute(query, additional)
                    results = cur.fetchall()
                    print(f'results: {results}')
                    if results is None:
                        return {}
                    return results

                except psycopg2.OperationalError as e:
                    print(f"Could not execute the query. Error: {e}")

        except psycopg2.OperationalError as e:
            print(f"Could not connect to the database. Error: {e}")


def query_insert_values(request_to_do:str=None, additional=None) -> None:
    """
    Executes an SQL query to insert values into the database based on the given request.

    Args:
        request_to_do (str): The type of request to perform. Possible values are:
            - 'create_new_account': Inserts a new account into the 'accounts' table.
            - 'delete_account': Deletes an account from the 'accounts' table.
            - 'create_new_budget': Inserts a new budget into the 'budgets' table.
            - 'delete_budget': Deletes a budget from the 'budgets' table.
            - 'create_new_transaction': Inserts a new transaction into the 'transactions' table.
            - 'apply_transaction_to_budget': Updates the 'amount' field of a budget in the 'budgets' table.
            - 'apply_transaction_to_accounts': Updates the 'balance' field of one or two accounts in the 'accounts' table.

        additional (tuple): Additional parameters required for the query. The contents of the tuple depend on the request type.

    Returns:
        None: This function does not return any value.

    Raises:
        psycopg2.OperationalError: If there is an error executing the query or connecting to the database.
    """
    additional = transform_additional(additional)

    # initialize query
    if request_to_do == 'create_new_account':
        query = 'INSERT INTO accounts (id, name, type, balance, owner) VALUES (%s, %s, %s, %s, %s)'
    if request_to_do == 'delete_account':
        query = 'DELETE FROM accounts WHERE id=%s'

    if request_to_do == 'create_new_budget':
        query = 'INSERT INTO budgets (id, name, month, amount) VALUES (%s, %s, %s, %s)'
    if request_to_do == 'delete_budget':
        query = 'DELETE FROM budgets WHERE id=%s'

    if request_to_do == 'create_new_transaction':
        query = 'INSERT INTO transactions (id, date, type, amount, origin_account, destination_account, budget, category, recipient, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    
    if request_to_do == 'delete_transaction':
        query = 'DELETE FROM transactions WHERE id=%s'

    if request_to_do == 'apply_transaction_to_budget':
        query = """
        UPDATE budgets 
        SET amount = amount - %s
        WHERE id = %s
        """

    if request_to_do == 'apply_transaction_to_accounts':
        # tuple to list
        additional_list = list(additional)
        # transaction type & remove it from additional
        type = additional[0]
        additional_list.pop(0)

        if type == 'credit':
            # Remove origin account from additional and convert back to tuple
            additional_list.pop(1)
            additional = tuple(additional_list)
            query = """
            UPDATE accounts
            SET balance = balance + %s
            WHERE name = %s
            """
        if type == 'debit':
            # Remove destination account from additional and convert back to tuple
            additional_list.pop(2)
            additional = tuple(additional_list)
            query = """
            UPDATE accounts
            SET balance = balance - %s
            WHERE name = %s
            """
        if type == 'transfert':
            # Extract values from additional
            transaction_amount, origin_account, destination_account = additional_list
            additional = (origin_account, transaction_amount, destination_account, transaction_amount, origin_account, destination_account)
            query = """
            UPDATE accounts
            SET balance = CASE 
                WHEN name = %s THEN balance - %s
                WHEN name = %s THEN balance + %s
                ELSE balance
            END
            WHERE name IN (%s, %s)
            """ 


    # Get engine
    engine = connect_to_db()


    # Apply Query
    with engine as conn:
        try:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                try:
                    cur.execute(query, additional)
                    conn.commit()

                except psycopg2.OperationalError as e:
                    print(f"Could not execute the query. Error: {e}")

        except psycopg2.OperationalError as e:
            print(f"Could not connect to the database. Error: {e}")