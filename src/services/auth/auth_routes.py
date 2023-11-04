from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from src.services.CRUD.Users_crud import get_user
from src.services.auth.auth import create_access_token
from src.services.password_hash import HashingPassword

router = APIRouter()


@router.post("/")
async def login_for_access_token(data: OAuth2PasswordRequestForm = Depends()):
    user_password = data.password
    user = await get_user(data.username)
    hashed_password = user.password
    print(user.password)
    if HashingPassword.is_hash_password_verify(user_password, hashed_password):
        return {"access_token": create_access_token(data.username), "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Wrong username or password")
