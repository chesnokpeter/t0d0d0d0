from abc import ABC, abstractmethod
from typing import TypeVar

RSAPrivate = TypeVar('RsaPrivate')
RSAPublic = TypeVar('RsaPublic')


class AbsEncryptionRepo(ABC):
    @abstractmethod
    def aes_encrypt(self, message: str, key: bytes) -> bytes:raise NotImplementedError

    @abstractmethod
    def aes_decrypt(self, message: bytes, key: bytes) -> bytes:raise NotImplementedError

    @abstractmethod
    def rsa_keys(self) -> tuple[RSAPrivate, RSAPublic]:raise NotImplementedError

    @abstractmethod
    def rsa_private_serial(self, private_key: RSAPrivate) -> bytes:raise NotImplementedError

    @abstractmethod
    def rsa_public_serial(self, public_key: RSAPublic) -> bytes:raise NotImplementedError

    @abstractmethod
    def rsa_private_deserial(self, private_key_pem: bytes) -> RSAPrivate:raise NotImplementedError

    @abstractmethod
    def rsa_public_deserial(self, public_key_pem: bytes) -> RSAPublic:raise NotImplementedError

    @abstractmethod
    def rsa_encrypt(self, message: str, public_key: RSAPublic) -> bytes:raise NotImplementedError

    @abstractmethod
    def rsa_decrypt(self, message: bytes, private_key: RSAPrivate) -> str:raise NotImplementedError

    @abstractmethod 
    def convert_tgid_to_aes_key(self, tgid: int) -> bytes:raise NotImplementedError

    @abstractmethod
    def hashed(self, data: str) -> str:raise NotImplementedError
