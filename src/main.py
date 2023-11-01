from fastapi import FastAPI, HTTPException, Request, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette.responses import JSONResponse

from src.services.CRUD.Users_crud import create_user, get_user
from src.db.models import User, UserResponse
from src.services.auth.auth import create_access_token, decode_access_token
from src.services.password_hash import HashingPassword

import pdb
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@app.get("/users/{username}", response_model=UserResponse)
async def read_user(username: str):
    user = await get_user(username)
    user_without_password = UserResponse(
        username=user.username,
        name=user.name,
        surname=user.surname,
        phone_number=user.phone_number,
        email=user.email
    )
    return user_without_password


@app.post("/token")
async def login_for_access_token(data: OAuth2PasswordRequestForm = Depends()):
    user_password = data.password
    user = await get_user(data.username)
    hashed_password = user.password
    print(user.password)
    if HashingPassword.is_hash_password_verify(user_password, hashed_password):
        return {"access_token": create_access_token(data.username), "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Неправильное имя пользователя или пароль")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_access_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return user


@app.get("/secure-data")
async def get_secure_data(current_user: User = Depends(get_current_user)):
    # В этом роуте, только аутентифицированные пользователи могут получить доступ
    return {"message": "This is secure data"}

#, current_user: User = Depends(get_current_user)
@app.post("/users/", response_model=User)
async def create_user_endpoint(user: User):
    try:
        return await create_user(user)
    except Exception as e:
        return {"error": str(e)}

# @app.get("/protected")
# async def protected_route(token: str = Depends(oauth2_scheme)):
#     payload = decode_access_token(token)
#     return {"message": "Защищенный маршрут", "username": payload.get("username")}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)
