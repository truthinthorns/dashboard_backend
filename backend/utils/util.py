import scrypt
import os
from dotenv import load_dotenv

load_dotenv()
salt = os.getenv("SALT")

def hash_password(password: str):
    return scrypt.hash(password, salt)


def check_password(guessed_password: str, actual_password: str):
    hash1 = scrypt.hash(guessed_password, salt)
    hash2 = scrypt.hash(actual_password, salt)
    return hash1 == hash2

