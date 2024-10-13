import random
import string


def genAuthCode(length=4):
    characters = string.digits
    random_string = ''.join(random.choices(characters, k=length))
    return random_string


from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

# Функция для генерации ключа из Telegram ID
def generate_key_from_telegram_id(telegram_id):
    telegram_id_str = str(telegram_id).encode('utf-8')  # Преобразуем ID в байты
    salt = b'\x00' * 16  # Можно использовать фиксированную соль или генерировать её случайно
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Длина ключа 256 бит для AES-256
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(telegram_id_str)
    return key

# Функция шифрования
def encrypt_message(telegram_id, message):
    key = generate_key_from_telegram_id(telegram_id)
    print(key)
    
    # Генерация случайного IV (инициализационный вектор)
    iv = os.urandom(16)
    
    # Паддинг сообщения до длины, кратной 16 байтам
    padder = padding.PKCS7(128).padder()
    padded_message = padder.update(message.encode('utf-8')) + padder.finalize()

    # Создание шифра AES-CBC
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()

    return iv + ciphertext  # IV нужно передавать вместе с зашифрованным текстом

# Функция расшифрования
def decrypt_message(telegram_id, encrypted_message):
    key = generate_key_from_telegram_id(telegram_id)
    
    iv = encrypted_message[:16]
    ciphertext = encrypted_message[16:]
    
    # Создание шифра AES-CBC для расшифрования
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_message = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    message = unpadder.update(padded_message) + unpadder.finalize()

    return message.decode('utf-8')

telegram_id = 123456789  # Telegram ID (9-11 цифр)
message = "Привет, как дела?"

encrypted_message = encrypt_message(telegram_id, message)
print("Зашифрованное сообщение:", encrypted_message)

decrypted_message = decrypt_message(telegram_id, encrypted_message)
print("Расшифрованное сообщение:", decrypted_message)