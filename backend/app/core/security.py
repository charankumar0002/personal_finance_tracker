# backend/app/core/security.py
from passlib.context import CryptContext

# Use bcrypt: a proven, secure hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a plain-text password.
    Returns the bcrypt hash (including salt).
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify that the plain_password matches the stored hashed_password.
    Returns True if they match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
