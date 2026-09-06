import hashlib
from src.db import users_collection

def hash_password(password: str) -> str:
    """Hash a plaintext password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def seed_default_users():
    """Seed the MongoDB database with default Admin and Support Agent users if empty."""
    if users_collection.count_documents({}) == 0:
        default_users = [
            {
                "username": "admin",
                "password_hash": hash_password("admin123"),
                "role": "Admin",
                "name": "System Administrator"
            },
            {
                "username": "agent",
                "password_hash": hash_password("agent123"),
                "role": "Support Agent",
                "name": "Support Agent"
            }
        ]
        users_collection.insert_many(default_users)

def authenticate_user(username: str, password: str):
    """Verify credentials against MongoDB and return user document if valid."""
    seed_default_users()  # Ensure initial accounts exist
    hashed = hash_password(password)
    user = users_collection.find_one({"username": username, "password_hash": hashed}, {"_id": 0})
    return user