import base64
import bcrypt
from cryptography import fernet
from cryptography.hazmat import backends
from cryptography.hazmat import primitives
from cryptography.hazmat.primitives.kdf import pbkdf2


def key_generator(password: str) -> bytes:
    """Return a sequence of bytes representing a generated key
    from the <password>.
    """

    password_encoded = password.encode()
    key_deriver = pbkdf2.PBKDF2HMAC(
        algorithm=primitives.hashes.SHA256(),
        length=32,
        salt=b'\xbf\x07\xfc\xb2Y\x80\xbas\xb4\x02\x0f\x84\x9da\xb3\xfb',
        iterations=100000,
        backend=backends.default_backend()
        )
    return base64.urlsafe_b64encode(key_deriver.derive(password_encoded))


def encrypt_password(password: str, key: bytes) -> str:
    """
    Return a string representing the encrypted <password> given the <key>.
    """

    fernet_object = fernet.Fernet(key)
    return fernet_object.encrypt(password.encode()).decode('utf-8')


def decrypt_password(encrypted_pass: str, key: bytes) -> str:
    """
    Return the decrypted password given <encrypted_pass> and the
    <key>.
    """

    fernet_object = fernet.Fernet(key)
    return fernet_object.decrypt(encrypted_pass.encode()).decode('utf-8')


def hash_password(password: str) -> bytes:
    """Return a sequence of bytes representing a hashed <password>."""

    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
