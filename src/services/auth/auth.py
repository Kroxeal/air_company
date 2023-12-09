import secrets
import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, Request
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from src.services.auth.Auth2PasswordCookie import OAuth2PasswordBearerWithCookie
from src.db.models import User, UserPatch

load_dotenv()

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = os.getenv('ALGORITHM')
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/auth/i")


def create_access_token(username: str, role: str):
    print("Creating access token")
    to_encode = {'sub': username, 'role': role}
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(request: Request):
    token = request.cookies.get("access_token")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print('payload')
        print(payload)
        return payload
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")


async def get_current_user(request: Request):
    user = decode_access_token(request)
    print('user_encode')
    print(user)
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return user


async def get_current_userr(current_user: dict = Depends(get_current_user)):
    print('before role')
    if current_user.get("role") != "user":
        print('in role')
        raise HTTPException(status_code=400, detail="Inactive user")
    print('hilo current_userr')
    return current_user


async def get_current_employee(current_user: dict = Depends(get_current_user)):
    print('employee')
    if current_user.get("role") != "employee":
        raise HTTPException(status_code=403, detail="Permission denied")
    return current_user


async def get_current_admin(current_user: dict = Depends(get_current_user)):
    print('admin')

    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")
    return current_user

