"""
PostGres Database connectors for the API
"""


"""
LIBS
"""
import asyncpg
import os


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
async def connect_to_db() -> asyncpg.connection:
    """
    Connects to the database using the provided credentials.

    Returns:
        asyncpg.connection: The connection object representing the connection to the database.
    """
    return await asyncpg.connect(user=postgres_user,
                                   password=postgres_password,
                                   database=postgres_db,
                                   host=postgres_host,
                                   port=postgres_port)




async def transform_additional(additional) -> tuple:
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



async def query_for_informations(request_to_do: str = None,
                                 additional = None) -> dict:
    """
    Executes a database query based on the given request_to_do and additional parameters.

    Args:
        request_to_do (str): The type of query to execute.
        additional: Additional parameters to be used in the query.

    Returns:
        dict: A dictionary containing the query results.

    Raises:
        ValueError: If an invalid request_to_do is provided.

    """
    additional = await transform_additional(additional)
    # Ensure additional is an iterable
    if additional is None:
        additional = []


    queries = {
        'get_username_informations': "SELECT * FROM users WHERE username=$1",
        'get_existing_accounts': 'SELECT * FROM accounts',
        'get_existing_budgets': 'SELECT * FROM budgets',
        'get_existing_transactions': 'SELECT * FROM transactions',
        'get_transaction_by_id': 'SELECT * FROM transactions WHERE id=$1',
        'get_existing_categories': 'SELECT DISTINCT category FROM transactions'
    }

    # Initialize query
    query = queries.get(request_to_do)
    if not query:
        raise ValueError(f"Invalid request_to_do: {request_to_do}")

    # Get engine
    engine = await connect_to_db()

    # Try connection & apply query
    try:
        async with engine.transaction():
            results = await engine.fetch(query, *additional)
            return [dict(record) for record in results]
        
    except Exception as e:
        print(f"Could not execute the query. Error: {e}")
        return {}
    
    finally:
        await engine.close()




async def query_insert_values(request_to_do: str = None, additional=None) -> None:
    additional = await transform_additional(additional)
    if additional is None:
        additional = []

    queries = {
        'create_new_account': 'INSERT INTO accounts (id, name, type, balance, owner) VALUES ($1, $2, $3, $4, $5)',
        'delete_account': 'DELETE FROM accounts WHERE id=$1',
        'create_new_budget': 'INSERT INTO budgets (id, name, month, amount) VALUES ($1, $2, $3, $4)',
        'delete_budget': 'DELETE FROM budgets WHERE id=$1',
        'create_new_transaction': 'INSERT INTO transactions (id, date, type, amount, origin_account, destination_account, budget, category, recipient, description) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)',
        'delete_transaction': 'DELETE FROM transactions WHERE id=$1',
        'apply_transaction_to_budget': 'UPDATE budgets SET amount = amount - $1 WHERE id = $2',
        'apply_transaction_to_accounts': """
            UPDATE accounts
            SET balance = CASE 
                WHEN name = $1 THEN balance - $2
                WHEN name = $3 THEN balance + $4
                ELSE balance
            END
            WHERE name IN ($1, $3)
        """
    }

    query = queries.get(request_to_do)
    if not query:
        raise ValueError(f"Invalid request_to_do: {request_to_do}")

    if request_to_do == 'apply_transaction_to_accounts':
        additional_list = list(additional)
        type = additional[0]
        additional_list.pop(0)

        if type == 'credit':
            additional_list.pop(1)
            additional = tuple(additional_list)
            query = """
            UPDATE accounts
            SET balance = balance + $1
            WHERE name = $2
            """

        if type == 'debit':
            additional_list.pop(2)
            additional = tuple(additional_list)
            query = """
            UPDATE accounts
            SET balance = balance - $1
            WHERE name = $2
            """

        if type == 'transfer':
            transaction_amount, origin_account, destination_account = additional_list
            additional = (origin_account, destination_account, transaction_amount)
            query = """
            UPDATE accounts
            SET balance = CASE 
                WHEN name = $1 THEN balance - $3
                WHEN name = $2 THEN balance + $3
                ELSE balance
            END
            WHERE name IN ($1, $2)
            """ 

    engine = await connect_to_db()

    try:
        async with engine.transaction():
            await engine.execute(query, *additional)
    except Exception as e:
        print(f"Could not execute the query. Error: {e}")
    finally:
        await engine.close()