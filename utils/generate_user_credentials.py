"""
Generate user credentials & add it to PostgreSQL database.
"""
# Version : 0.2.0
# Current state : Dev
# Author : Guillaume Pot
# Contact : guillaumepot.pro@outlook.com


# THIS SECTION NEEDS TO BE UPDATED
import os
import json
import time
from datetime import datetime
import getpass
from passlib.context import CryptContext

crypt_context_scheme = "argon2"


def generate_user_credentials() -> None:
    """
    Generate a username and password for a user.
    """
    # Load user file
    user_file_path = input("Enter the path to the user file: (Ex: ../storage/users.json)")

    if os.path.exists(user_file_path):
        with open(user_file_path, 'r') as user_file:
            all_user_datas = json.load(user_file)
    else:
        all_user_datas = {}

    # Get username
    username = input("Enter a username: ")


    # Check if user already exists
    if username in all_user_datas:
        raise ValueError("User already exists")

    # Get password & encrypt
    password = getpass.getpass("Enter a password: ")
    pwd_context = CryptContext(schemes=[crypt_context_scheme], deprecated="auto")
    hashed_password = pwd_context.hash(password)

    # Create user
    user_datas = {}
    user_datas["password"] = hashed_password
    user_datas["role"] = 0
    user_datas["created_at"] = time.mktime(datetime.now().timetuple())
    all_user_datas[username] = user_datas


    with open(user_file_path, "w") as file:
        json.dump(all_user_datas, file, indent=4)

    print(f"User {username} succefully registered.")


if __name__ == "__main__":
    generate_user_credentials()


# CLI example
# python3 generate_user_credentials.py