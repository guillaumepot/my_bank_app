"""
Generate a secret key and store it in a file
"""

# Version : 0.1.0
# Current state : Dev
# Author : Guillaume Pot
# Contact : guillaumepot.pro@outlook.com



from cryptography.fernet import Fernet

def generate_secret_key() -> None:
    """
    Generates a secret key using the Fernet encryption algorithm and sets it as the value of the BANK_APP_API_TOKEN_SECRET_KEY environment variable.

    Returns:
        None
    """
    key = Fernet.generate_key()
    print(key.decode())

if __name__ == "__main__":
    generate_secret_key()

# CLI example
# export BANK_APP_API_TOKEN_SECRET_KEY=$(python3 ./utils/generate_secret_key.py)