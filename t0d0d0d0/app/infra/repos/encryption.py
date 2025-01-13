from os import urandom
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding as paddingasy

from ...domain.repos import AbsEncryptionRepo
from ...domain.repos.base import NonSession

class EncryptionRepoHazmat(AbsEncryptionRepo[NonSession]):
    depends_on = None

    def __init__(self, session: NonSession):...


    def aes_encrypt(self, message: str, key: bytes) -> bytes:
        iv = urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(message.encode()) + padder.finalize()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return iv + ciphertext



    def aes_decrypt(self, message: bytes, key: bytes) -> bytes:
        iv = message[:16]
        message = message[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(message) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        return plaintext






    def rsa_keys(self, ) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key



    def rsa_private_serial(self, private_key: rsa.RSAPrivateKey) -> bytes:
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()  
        )
        return private_key_pem

    def rsa_public_serial(self, public_key: rsa.RSAPublicKey) -> bytes:
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return public_key_pem


    def rsa_private_deserial(self, private_key_pem: bytes) -> rsa.RSAPrivateKey:
        return serialization.load_pem_private_key(
            private_key_pem,
            password=None,
            backend=default_backend()
        )

    def rsa_public_deserial(self, public_key_pem: bytes) -> rsa.RSAPublicKey:
        return serialization.load_pem_public_key(
            public_key_pem,
            backend=default_backend()
        )



    def rsa_encrypt(self, message: str, public_key: rsa.RSAPublicKey) -> bytes:
        ciphertext = public_key.encrypt(
            message.encode('utf-8'),
            paddingasy.OAEP(
                mgf=paddingasy.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext



    def rsa_decrypt(self, message: bytes, private_key: rsa.RSAPrivateKey) -> str:
        plaintext = private_key.decrypt(
            message,
            paddingasy.OAEP(
                mgf=paddingasy.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext.decode('utf-8')



    def hashed(self, message: str, algorithm: hashes.HashAlgorithm = hashes.SHA256()) -> bytes:
        digest = hashes.Hash(algorithm, backend=default_backend())
        digest.update(message.encode())
        return digest.finalize()
    
    def convert_tgid_to_aes_key(self, tgid: int, len:int=32) -> bytes:
        return tgid.to_bytes(len)

