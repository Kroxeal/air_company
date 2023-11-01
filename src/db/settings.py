import os
from dotenv import load_dotenv

from src.db.connection import Database

load_dotenv()


database = Database(
    user=os.getenv('USERNAME_DB'),
    password=os.getenv('PASSWORD'),
    database=os.getenv('DATABASE'),
    host=os.getenv('HOST'),
    port=os.getenv('PORT'),
)
