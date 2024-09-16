import re
import os
from bson.objectid import ObjectId
from cryptography.fernet import Fernet
from db_connector import get_db

class PasswordVault:
    def __init__(self, session):
        self.session = session
        self.db = get_db()
        self.vaults_collection = self.db['vaults']

    def __encrypt_password(self, user_key, password):
        cipher_suite = Fernet(user_key)
        return cipher_suite.encrypt(password.encode()).decode()

    def __decrypt_password(self, user_key, encrypted_password):
        cipher_suite = Fernet(user_key)
        return cipher_suite.decrypt(encrypted_password.encode()).decode()
    
    def __validate_password(self, password):
        # Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character
        if (len(password) < 8 or
            not re.search(r'[A-Z]', password) or
            not re.search(r'[a-z]', password) or
            not re.search(r'[0-9]', password) or
            not re.search(r'[\W_]', password)):
            return False
        return True

    def add_password(self, service, password):
        current_user = self.session.get_current_user()
        if not current_user:
            return "No user is currently logged in."

        user_key = self.session.get_user_key()
        encrypted_password = self.__encrypt_password(user_key, password)
        vault_entry = {
            "user_id": current_user["_id"],
            "service": service,
            "password": encrypted_password
        }
        self.vaults_collection.update_one(
            {"user_id": current_user["_id"], "service": service},
            {"$set": vault_entry},
            upsert=True
        )
        return f"Password for {service} added successfully."

    def get_password(self, service):
        current_user = self.session.get_current_user()
        if not current_user:
            return None, "No user is currently logged in."

        user_key = self.session.get_user_key()
        vault_entry = self.vaults_collection.find_one({"user_id": current_user["_id"], "service": service})
        if vault_entry:
            encrypted_password = vault_entry["password"]
            password = self.__decrypt_password(user_key, encrypted_password)
            is_secure = self.__validate_password(password)
            return password, is_secure
        return None, "No password found for this service."

    def list_services(self):
        current_user = self.session.get_current_user()
        if not current_user:
            return []

        services = self.vaults_collection.find({"user_id": current_user["_id"]}, {"service": 1, "_id": 0})
        return [service["service"] for service in services]

