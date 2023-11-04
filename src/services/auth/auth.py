import secrets
import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

load_dotenv()

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = os.getenv('ALGORITHM')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/")


def create_access_token(username: str):
    to_encode = {'sub': username}
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_access_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return user
