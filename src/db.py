import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "complaint_management_db")

if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable is missing. Check your .env file.")

# Initialize MongoDB Client
client = MongoClient(MONGO_URI)
db_instance = client[DB_NAME]

# Define Collections
complaints_collection = db_instance["complaints"]
users_collection = db_instance["users"]

def test_connection():
    """Utility to test if connection to MongoDB Atlas works."""
    try:
        client.admin.command('ping')
        print("Successfully connected to MongoDB Atlas!")
        return True
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()