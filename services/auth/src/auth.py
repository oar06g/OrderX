from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY_JWT

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plaintext password using a secure hashing algorithm."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(data: dict):
    """Create JWT Token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY_JWT, algorithm=ALGORITHM)
    return token

def decode_jwt_token(token: str):
    return jwt.decode(token, SECRET_KEY_JWT, algorithms=[ALGORITHM])
