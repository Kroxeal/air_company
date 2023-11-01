from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()


class HashingPassword:
    scheme_hashing = os.getenv('SCHEME_HASHING')
    PWD_CONTEXT = CryptContext(schemes=[scheme_hashing], deprecated="auto")

    @staticmethod
    def password_to_hash(password):
        hashed_password = HashingPassword.PWD_CONTEXT.hash(password)
        return hashed_password

    @staticmethod
    def is_hash_password_verify(user_password, hashed_password):
        status = HashingPassword.PWD_CONTEXT.verify(user_password, hashed_password)
        return status
