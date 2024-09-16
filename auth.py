import re
import hashlib
import os
from bson.objectid import ObjectId
from key_manager import UserKeysManager
from db_connector import get_db
from session import Session

class AuthSystem:

    def __init__(self):
        self.db = get_db()
        self.users_collection = self.db["users"]
        self.crypto_manager =  UserKeysManager()
        self.session = Session()

    def __validate_password(self, password):

        if (
            len(password) < 8
            or not re.search(r"[A-Z]", password)
            or not re.search(r"[a-z]", password)
            or not re.search(r"[0-9]", password)
            or not re.search(r"[\W_]", password)
        ):
            return False
        return True

    def register(self, username, password):

        # Check if username already exists
        if self.users_collection.find_one({"username": username}):
            return "Username already exists."

        if not self.__validate_password(password):
            Exception("Password must be at least 8 characters long and contain an uppercase letter, a lowercase letter, a digit, and a special character.")

        # Generate user key and encrypt it
        user_key = self.crypto_manager.generate_key()
        encrypted_user_key = self.crypto_manager.encrypt(user_key)

        # Add new user with hashed password and encrypted user key
        new_user = {
            "username": username,
            "password": hashlib.sha256(password.encode()).hexdigest(),
            "encrypted_user_key": encrypted_user_key,
        }
        result = self.users_collection.insert_one(new_user)
        return "User registered successfully."

    def login(self, username, password):

        # Hash the input password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check if username and hashed password match any registered user
        user = self.users_collection.find_one(
            {"username": username, "password": hashed_password}
        )
        if user:
            # Decrypt the user's key
            encrypted_user_key = user["encrypted_user_key"]
            user_key = self.crypto_manager.decrypt(encrypted_user_key)
            self.session.login(user, user_key)
            return "Login successful."
        return "Invalid username or password."

    def logout(self):
        self.session.logout()
        return "Logout successful."


# Example usage
if __name__ == "__main__":
    auth_system = AuthSystem()
    print(auth_system.register("user1", "Password1!"))  # User registered successfully.
    print(auth_system.login("user1", "Password1!"))  # Login successful.
    print(auth_system.session.get_current_user())  # Get current user details
    print(auth_system.logout())  # Logout successful.
    print(auth_system.session.get_current_user())
