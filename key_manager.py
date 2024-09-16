import os
from cryptography.fernet import Fernet

class UserKeysManager:
    def __init__(self):
        self.master_key_path = 'master.key'
        self.master_key = self.load_master_key()
        self.master_cipher_suite = Fernet(self.master_key)

    def load_master_key(self):
        # Load or generate master key
        if os.path.exists(self.master_key_path):
            with open(self.master_key_path, 'rb') as key_file:
                return key_file.read()
        else:
            key = Fernet.generate_key()
            with open(self.master_key_path, 'wb') as key_file:
                key_file.write(key)
            return key

    def generate_key(self):
        # Generate a new Fernet key
        return Fernet.generate_key()

    def encrypt(self, data):
        # Encrypt data using master cipher suite
        return self.master_cipher_suite.encrypt(data).decode()

    def decrypt(self, encrypted_data):
        # Decrypt encrypted data using master cipher suite
        return self.master_cipher_suite.decrypt(encrypted_data.encode()).decode()
