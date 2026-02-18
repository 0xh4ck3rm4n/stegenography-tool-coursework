from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os


def derive_key_from_password(password: str, salt: bytes = None) -> tuple:

    if salt is None:
        salt = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt


def encrypt_message(message: str, password: str) -> bytes:

    key, salt = derive_key_from_password(password)
    cipher = Fernet(key)
    encrypted = cipher.encrypt(message.encode())

    # Prepend salt to encrypted data for decryption later
    return salt + encrypted


def decrypt_message(encrypted_data: bytes, password: str) -> str:

    try:
        # Extract salt (first 16 bytes)
        salt = encrypted_data[:16]
        encrypted_message = encrypted_data[16:]

        key, _ = derive_key_from_password(password, salt)
        cipher = Fernet(key)
        decrypted = cipher.decrypt(encrypted_message)

        return decrypted.decode()
    except (InvalidToken, Exception):
        return None


def encrypt_bytes(data: bytes, password: str) -> bytes:
    key, salt = derive_key_from_password(password)
    cipher = Fernet(key)
    encrypted = cipher.encrypt(data)

    return salt + encrypted


def decrypt_bytes(encrypted_data: bytes, password: str) -> bytes:
    try:
        salt = encrypted_data[:16]
        encrypted_message = encrypted_data[16:]

        key, _ = derive_key_from_password(password, salt)
        cipher = Fernet(key)
        decrypted = cipher.decrypt(encrypted_message)

        return decrypted
    except (InvalidToken, Exception):
        return None
