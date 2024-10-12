from kbrainsdk.apibase import APIBase
from cryptography.fernet import Fernet

class KBRaiNEncryption():
    
    def generate_key(self):
        key = Fernet.generate_key()
        return key

    def encrypt(self, plaintext: str, key: bytes) -> bytes:
        fernet = Fernet(key)
        cipher_text = fernet.encrypt(plaintext.encode())
        return cipher_text

    def decrypt(self, cipher_text: bytes, key: bytes) -> str:
        fernet = Fernet(key)
        plaintext = fernet.decrypt(cipher_text).decode()
        return plaintext