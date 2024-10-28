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

