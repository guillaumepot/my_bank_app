import os
import json
import getpass
from passlib.context import CryptContext

crypt_context_scheme = "argon2"
user_file_path = "./src/storage/users.json"


def generate_user_credentials() -> None:
    """
    Generate a username and password for a user.
    """
    # Load user file
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
    all_user_datas[username] = user_datas


    with open(user_file_path, "w") as file:
        json.dump(all_user_datas, file, indent=4)

    print(f"User {username} succefully registered.")


if __name__ == "__main__":
    generate_user_credentials()

# CLI example
# python3 ./utils/generate_user_credentials.py