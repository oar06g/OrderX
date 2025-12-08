from jose import jwt, JWTError
from src.settings import ALGORITHM, SECRET_KEY_JWT

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY_JWT, algorithms=[ALGORITHM])
        return payload
    except JWTError: return None