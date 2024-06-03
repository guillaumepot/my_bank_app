"""
Generate table in a PostgreSQL database
"""
# Version : 0.1.0
# Current state : Dev
# Author : Guillaume Pot
# Contact : guillaumepot.pro@outlook.com

import argparse
import psycopg2



# Args parser
parser = argparse.ArgumentParser(description='Generate tables in a PostgreSQL database')
parser.add_argument('--user', type=str, help='Username to log in the database')
parser.add_argument('--password', type=str, help='Password to log in the database')
parser.add_argument('--db', type=str, help='Database name')
parser.add_argument('--host', type=str, help='Database host')
parser.add_argument('--port', type=str, help='Database port')

params = parser.parse_args()



def main(params):
    """
    Generate tables for the bank application.

    Args:
        params (object): An object containing the necessary parameters for connecting to the database.

    Returns:
        None
    """
    # Get args
    user = params.user
    password = params.password
    db = params.db
    host = params.host
    port = params.port

    # Connect Database
    conn = psycopg2.connect(
        dbname=db,
        user=user,
        password=password,
        host=host,
        port=port
    )

    # Create a cursor
    cur = conn.cursor()



    # Create tables

    # User table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(255) PRIMARY KEY,
            password VARCHAR(255) NOT NULL,
            role INTEGER NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Account table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id UUID PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            type VARCHAR(255) NOT NULL,
            balance FLOAT CHECK(balance >= 0) NOT NULL,  
            owner VARCHAR(255) REFERENCES users(username),
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            deleted_at TIMESTAMP,
            history JSONB
        )
    """)

    # Budget table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id UUID PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            month VARCHAR(255) NOT NULL,
            amount FLOAT CHECK(amount >= 0) NOT NULL,
            history JSONB,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            deleted_at TIMESTAMP,
            history JSONB
        )
    """)

    # Transaction table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id UUID PRIMARY KEY,
            date DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            type VARCHAR(255) CHECK(type IN ('debit', 'credit', 'transfert')) NOT NULL,
            amount FLOAT CHECK(amount >= 0) NOT NULL,
            origin_account UUID,
            destination_account UUID,
            budget UUID,
            category VARCHAR(255),
            description TEXT,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            deleted_at TIMESTAMP
        )
    """)

    # Validate Changes
    conn.commit()

    # Close connection
    cur.close()
    conn.close()


if __name__ == '__main__':
    main(params)