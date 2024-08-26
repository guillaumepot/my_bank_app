-- init.sql
\c bank_db

-- Create tables


-- User table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- Account table
CREATE TABLE IF NOT EXISTS accounts (
    id UUID PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    balance FLOAT NOT NULL,  
    owner UUID REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- Budget table
CREATE TABLE IF NOT EXISTS budgets (
    id UUID PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    month VARCHAR(255) NOT NULL,
    amount FLOAT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Add budget with ID 0 and month "N/A" for the default budget (no budget)
INSERT INTO budgets (id, name, month, amount)
VALUES ('00000000-0000-0000-0000-000000000000', 'default', 'N/A', 0)
ON CONFLICT DO NOTHING;



-- Transaction table
CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY NOT NULL,
    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    type VARCHAR(255) CHECK(type IN ('debit', 'credit', 'transfert')) NOT NULL,
    amount FLOAT CHECK(amount >= 0) NOT NULL,
    origin_account VARCHAR(255),
    destination_account VARCHAR(255),
    budget UUID REFERENCES budgets(id),
    recipient VARCHAR(255) NOT NULL,
    category VARCHAR(255),
    description TEXT
);