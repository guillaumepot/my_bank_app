"""
Generate table in a PostgreSQL database
"""
import psycopg2


# Get credentials to log in the database
user = input("Enter your username: ")
password = input("Enter your password: ") 



# Connect Database
conn = psycopg2.connect(
    dbname="bank_db",
    user=user,
    password=password,
    host="bank_app_postgres",
    port="5432"
)

# Create a cursor
cur = conn.cursor()


# Create tables

# User table
cur.execute("""
    CREATE TABLE users IF NOT EXISTS (
        username VARCHAR(255) PRIMARY KEY,
        password VARCHAR(255) NOT NULL,
        role INTEGER NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    )
""")


# Account table
cur.execute("""
    CREATE TABLE accounts IF NOT EXISTS (
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
    CREATE TABLE budgets IF NOT EXISTS (
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
    CREATE TABLE transactions IF NOT EXISTS (
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