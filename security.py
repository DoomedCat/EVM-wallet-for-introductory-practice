import bcrypt
import json
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64


class Security:
    @staticmethod
    def set_password(password: str) -> None:
        with open("security_config.json", "r") as file:
            security_dict = json.load(file)
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        security_dict["password"] = hashed_password.decode('utf-8')
        with open("security_config.json", "w") as file:
            json.dump(security_dict, file)

    @staticmethod
    def compare_password(password: str) -> bool:
        with open("security_config.json", "r") as file:
            hashed_password = json.load(file)["password"].encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    @staticmethod
    def set_private_key(private_key: str, password: str):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
        cipher_suite = Fernet(key)
        cipher_text = cipher_suite.encrypt(private_key.encode('utf-8'))
        with open("security_config.json", "r") as file:
            security_dict = json.load(file)
        security_dict["private_key"] = base64.urlsafe_b64encode(salt + cipher_text).decode('utf-8')
        with open("security_config.json", "w") as file:
            json.dump(security_dict, file)

    @staticmethod
    def get_private_key(password: str) -> str:
        with open("security_config.json", "r") as file:
            encrypted_data = base64.urlsafe_b64decode(json.load(file)["private_key"].encode('utf-8'))
        salt = encrypted_data[:16]
        cipher_text = encrypted_data[16:]
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
        cipher_suite = Fernet(key)
        plain_text = cipher_suite.decrypt(cipher_text)
        return plain_text.decode('utf-8')

    @staticmethod
    def reset_data():
        stamp = {"password": "", "private_key": ""}
        with open("security_config.json", "w") as file:
            json.dump(stamp, file)
