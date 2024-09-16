from pymongo import MongoClient
from dotenv import load_dotenv
import os

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            load_dotenv()  # Load environment variables from .env file
            database_url = os.getenv('DATABASE_URL')
            if not database_url:
                raise ValueError("DATABASE_URL environment variable not set")
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.client = MongoClient(database_url)
            cls._instance.db = cls._instance.client['auth_system_db']
        return cls._instance

    def get_db(self):
        return self.db

# Usage
def get_db():
    return Database().get_db()

if __name__ == "__main__":
    try:
        db = get_db()
        print("Database instance created.")
    except Exception as e:
        print("Error: ", e)
