import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key

class UserKeysManager:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        self.master_key = self.__load_master_key()
        self.master_cipher_suite = Fernet(self.master_key)

    def __load_master_key(self):
        # Load master key from environment variable or generate a new one
        master_key = os.getenv('MASTER_KEY')
        if master_key:
            return master_key.encode()
        else:
            key = Fernet.generate_key()
            self.__save_master_key_to_env(key)
            return key

    def __save_master_key_to_env(self, key):
        # Save the generated master key to the .env file
        env_file = '.env'
        set_key(env_file, 'MASTER_KEY', key.decode())


    def encrypt(self, data):
        # Encrypt data using master cipher suite
        return self.master_cipher_suite.encrypt(data).decode()

    def decrypt(self, encrypted_data):
        # Decrypt encrypted data using master cipher suite
        return self.master_cipher_suite.decrypt(encrypted_data.encode()).decode()
