import random
import string
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding

def genAuthCode(length=4):
    characters = string.digits
    random_string = ''.join(random.choices(characters, k=length))
    return random_string


def convert_tgid_to_aes_key(tgid: int, len:int=32) -> bytes:
    return tgid.to_bytes(len)

def aes_encrypt(message: str, key: str) -> bytes:
    key = key.encode('utf-8')
    salt = b'\x00' * 16
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(key)
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_message = padder.update(message.encode('utf-8')) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()
    return iv + ciphertext

def aes_decrypt(message: str, key: str) -> str:
    key = key.encode('utf-8')
    salt = b'\x00' * 16
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(key)
    iv = message[:16]
    ciphertext = message[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_message = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    message = unpadder.update(padded_message) + unpadder.finalize()
    return message.decode('utf-8')

def rsa_generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def rsa_encrypt(public_key, message):
    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def rsa_decrypt(private_key, ciphertext):
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext

# telegram_id = 821785013
# message = "Привет, как дела?"

# encrypted_message = aes_encrypt(message, str(telegram_id))
# print("Зашифрованное сообщение:", encrypted_message)

# dectypt = aes_decrypt(encrypted_message, str(telegram_id))
# print('расшифрованное: ', dectypt)

# test = b'hello kak dela'
# private, public = rsa_generate_keys()
# enc = rsa_encrypt(public, test)
# print(enc)
# dec = rsa_decrypt(private, enc)
# print(dec)



def encrypt_aes(plaintext: str, key: bytes) -> bytes:
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext


def decrypt_aes(ciphertext: bytes, key: bytes) -> str:
    iv = ciphertext[:16]
    actual_ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext.decode()

# # Пример расшифровки
# key = os.urandom(32)  # 256-битный ключ для AES-256
# key = 821785013
# plaintext = "Это секретное сообщение"
# ciphertext = encrypt_aes(plaintext, key.to_bytes(32))
# print(f"Зашифрованное сообщение: {str(ciphertext)}")
# decrypted_text = decrypt_aes(ciphertext, key.to_bytes(32))
# print(f"Расшифрованное сообщение: {decrypted_text}")
# # Пример использования


# 1. Генерация ключей RSA
def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,  # Можно выбрать 2048 или 4096 для большей безопасности
        backend=default_backend()
    )
    public_key = private_key.public_key()
    
    return private_key, public_key

# 2. Шифрование сообщения с использованием открытого ключа
def encrypt_rsa(plaintext: str, public_key) -> bytes:
    ciphertext = public_key.encrypt(
        plaintext.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

# 3. Расшифровка сообщения с использованием закрытого ключа
def decrypt_rsa(ciphertext: bytes, private_key) -> str:
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode()

# Пример использования
private_key, public_key = generate_rsa_keys()

plaintext = "Это секретное сообщение"
ciphertext = encrypt_rsa(plaintext, public_key)
print(f"Зашифрованное сообщение: {ciphertext}")

decrypted_text = decrypt_rsa(ciphertext, private_key)
print(f"Расшифрованное сообщение: {decrypted_text}")