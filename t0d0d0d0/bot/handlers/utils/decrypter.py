from ....app.domain.repos.encryption import AbsEncryptionRepo, RSAPrivate

class FDecrypter:...



def decrypt(message: bytes, key: RSAPrivate, repo: AbsEncryptionRepo) -> str:
    return repo.rsa_decrypt(message, key)




