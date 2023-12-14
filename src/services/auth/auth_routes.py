from fastapi import Depends, HTTPException, APIRouter, Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from src.db.models import UserRegistration, PostUser
from src.services.CRUD.Users_crud import get_user, create_user
from src.services.auth.auth import create_access_token, oauth2_scheme
from src.services.password_hash import HashingPassword

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/i")
async def login_for_access_token(data: OAuth2PasswordRequestForm = Depends()):
    print("hello login")
    user_password = data.password
    user = await get_user(data.username)
    hashed_password = user.password
    print(user)
    print(user.password)
    if HashingPassword.is_hash_password_verify(user_password, hashed_password):
        return {
            "access_token": create_access_token(data.username, user.role),
            "token_type": "bearer"
        }
    raise HTTPException(status_code=400, detail="Wrong username or password")


@router.get("/i")
async def get_login_page(request: Request):
    return templates.TemplateResponse("auth/user.html", {"request": request})


@router.post("/logout")
async def logout(response: JSONResponse):
    response.delete_cookie("access_token")
    return {"message": "Logout successful"}


@router.post('/registration')
async def registration_post(user: PostUser):
    user.role = "user"
    result = await create_user(user)
    return result


@router.get('/registration')
async def registration(request: Request):
    context = {
        'request': request,
    }
    return templates.TemplateResponse('auth/registration.html', context=context)
