from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "bfa5ec7c8b2649a09b4e0167df1e3af851e2c517e6a8f09d047c98d639ad0e1c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
