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



def query_pg_db(request_to_do:str=None, additional=None, return_attended = 'yes') -> dict:
    """
    Query the Postgres Database
    """
    if isinstance(additional, str):
        additional = (additional,)


    # initialize query
    if request_to_do == 'get_username_informations':
        query = "SELECT * FROM users WHERE username=%s"

    if request_to_do == 'get_existing_accounts':
        query = 'SELECT name FROM accounts'
    
    if request_to_do == 'create_new_account':
        query = 'INSERT INTO accounts (id, name, type, balance, owner, history) VALUES (%s, %s, %s, %s, %s, %s)'


    # initialize connexion
    with psycopg2.connect(dbname=postgres_db,
                          user=postgres_user,
                          password=postgres_password,
                          host=postgres_host,
                          port=postgres_port) as conn:
            
            try:
                with conn.cursor(cursor_factory=DictCursor) as cur:
                    # execute query
                    cur.execute(query, additional)

                    # If the route is a GET, return the result
                    if return_attended == 'yes':
                        result = cur.fetchall()
                        if result == None:
                            result = {}
                            return result
                        else:
                            return dict(result)
                    
                    # If the route is a POST or DELETE
                    else:
                        conn.commit()


            except psycopg2.OperationalError as e:
                print(f"Could not connect to the database. Error: {e}")