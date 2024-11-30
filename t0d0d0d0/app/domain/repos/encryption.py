from abc import ABC, abstractmethod
from typing import TypeVar

RSAPrivate = TypeVar('RsaPrivate')
RSAPublic = TypeVar('RsaPublic')


class AbsEncryptionRepo(ABC):
    @abstractmethod
    def aes_encrypt(message: str, key: bytes) -> bytes:raise NotImplementedError

    @abstractmethod
    def aes_decrypt(message: bytes, key: bytes) -> bytes:raise NotImplementedError

    @abstractmethod
    def rsa_keys() -> tuple[RSAPrivate, RSAPublic]:raise NotImplementedError

    @abstractmethod
    def rsa_private_serial(private_key: RSAPrivate) -> bytes:raise NotImplementedError

    @abstractmethod
    def rsa_public_serial(public_key: RSAPublic) -> bytes:raise NotImplementedError

    @abstractmethod
    def rsa_private_deserial(private_key_pem: bytes) -> RSAPrivate:raise NotImplementedError

    @abstractmethod
    def rsa_public_deserial(public_key_pem: bytes) -> RSAPublic:raise NotImplementedError

    @abstractmethod
    def rsa_encrypt(message: str, public_key: RSAPublic) -> bytes:raise NotImplementedError

    @abstractmethod
    def rsa_decrypt(message: bytes, private_key: RSAPrivate) -> str:raise NotImplementedError


