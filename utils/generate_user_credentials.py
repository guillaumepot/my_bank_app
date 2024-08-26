"""
Generate user credentials & add it to PostgreSQL database.
"""

# LIBS
import uuid
import getpass
import argparse
import psycopg2
from passlib.context import CryptContext


# Crypt context
crypt_context_scheme = "argon2"



# Args parser
parser = argparse.ArgumentParser(description='Generate tables in a PostgreSQL database')
parser.add_argument('--user', type=str, help='Username to log in the database')
parser.add_argument('--password', type=str, help='Password to log in the database')
parser.add_argument('--db', type=str, help='Database name')
parser.add_argument('--host', type=str, help='Database host')
parser.add_argument('--port', type=str, help='Database port')


params = parser.parse_args()


# MAIN FUNCTION

def main(params) -> None:
    """
    Generate a username and password for a user and add it into postgresql database.
    """
    # Get args
    user = params.user
    password = params.password
    db = params.db
    host = params.host
    port = params.port

    # Connect Database
    try:
        with psycopg2.connect(
        dbname=db,
        user=user,
        password=password,
        host=host,
        port=port
    ) as conn:
            # Create a cursor
            with conn.cursor() as cur:
                # Get Username
                username = input('Enter the username: ')
                # Get password
                while True:
                    user_password = getpass.getpass('Enter the password: ')
                    confirm_password = getpass.getpass('Confirm the password: ')
                    if user_password == confirm_password:
                        break
                    else:
                        print("Passwords don't match.")

                user_role = 0
                user_id = str(uuid.uuid4())

                # Check if user exists
                cur.execute("SELECT * FROM users WHERE username=%s", (username,))
                user = cur.fetchone()
                if user:
                    raise ValueError("User already exists")


                # Encrypt password
                pwd_context = CryptContext(schemes=[crypt_context_scheme], deprecated="auto")
                hashed_password = pwd_context.hash(user_password)


                # Add user to DB
                cur.execute("""
                    INSERT INTO users (id, username, password, role)
                    VALUES (%s, %s, %s, %s)
                            """, (user_id, username, hashed_password, user_role))
                conn.commit()

                # Return success message
                print(f"User {username} succefully registered.")

    except psycopg2.OperationalError as e:
        print(f"Could not connect to the database. Error: {e}")


if __name__ == "__main__":
    main(params)

# CLI example
# python3 generate_user_credentials.py --user root --password 'password' --db bank_db --host localhost --port 5432