"""This module uses Bcrypt to encode the password sent by user"""

import bcrypt


def hash_password(password: str) -> str:
    """
    Convert a plain-text password into a secure cryptographic hash.

    Args:
        password: User Password

    Returns:
        Hashed Password in string

    """
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_password_bytes.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a stored database hash.
    Args:
        plain_password: User Password
        hashed_password: Hashed password from DB
    Returns:
        boolean for matched or not
    """
    plain_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(plain_bytes, hashed_bytes)
