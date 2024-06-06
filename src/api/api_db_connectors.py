#####
# TEMPORARY VARIABLES
#####
#
#
#
postgres_host="localhost"
postgres_port=5432
postgres_user="root"
postgres_password= "root"
postgres_db = 'bank_db'
#
#
#
#####
# END OF TEMPORARY VARIABLES
#####


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

# REMOVE COMMENT WHEN TEMP VARS ARE REMOVED
"""
postgres_host = os.getenv('POSTGRES_HOST')
postgres_port = os.getenv('POSTGRES_PORT')
postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_db = os.getenv('POSTGRES_DB')
"""


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
    if isinstance(additional, str):
        return (additional,)
    else:
        return additional



def query_for_informations(request_to_do:str=None, additional=None) -> dict:
    """
    
    """
    additional = transform_additional(additional)

    # Initialize query
    if request_to_do == 'get_username_informations':
        query = "SELECT * FROM users WHERE username=%s"

    if request_to_do == 'get_existing_accounts':
        query = 'SELECT * FROM accounts'

    if request_to_do == 'get_existing_budgets':
        query = 'SELECT * FROM budgets'



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
                    if results == None:
                        return {}
                    return results


                except psycopg2.OperationalError as e:
                    print(f"Could not execute the query. Error: {e}")

        except psycopg2.OperationalError as e:
            print(f"Could not connect to the database. Error: {e}")




def query_insert_values(request_to_do:str=None, additional=None) -> None:
    """
    
    """
    additional = transform_additional(additional)

    # initialize query
    if request_to_do == 'create_new_account':
        query = 'INSERT INTO accounts (id, name, type, balance, owner, history) VALUES (%s, %s, %s, %s, %s, %s)'
    if request_to_do == 'delete_account':
        query = 'DELETE FROM accounts WHERE id=%s'
    if request_to_do == 'create_new_budget':
        query = 'INSERT INTO budgets (id, name, month, amount, history) VALUES (%s, %s, %s, %s, %s)'
    if request_to_do == 'delete_budget':
        query = 'DELETE FROM budgets WHERE id=%s'


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

