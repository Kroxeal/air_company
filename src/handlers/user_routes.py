from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from src.db.models import User, UserResponse, BaseUser, UserPatch
from src.services.CRUD.Users_crud import create_user, get_user, update_user, update_user_partially, delete_user_f, \
    get_all_users
from src.services.auth.auth import get_current_admin, get_current_user, get_current_userr

router = APIRouter()
templates = Jinja2Templates(directory='templates')


# current_user: User = Depends(get_current_user)
@router.post("/", response_model=User)
async def create_user_endpoint(user: User):
    try:
        return await create_user(user)
    except Exception as e:
        return {"error": str(e)}


@router.get("/{username}", response_model=UserResponse)
async def read_user(username: str, current_user: UserPatch = Depends(get_current_userr)):
    print('hi read_user')
    user = await get_user(username)
    user_without_password = UserResponse(
        username=user.username,
        name=user.name,
        surname=user.surname,
        phone_number=user.phone_number,
        email=user.email
    )
    return user_without_password


@router.put("/{username}", response_model=BaseUser)
async def change_user(username: str, user: BaseUser):
    return await update_user(username, user)


@router.patch("/{username}", response_model=UserPatch)
async def update_user(username: str, user: UserPatch):
    return await update_user_partially(username, user)


@router.delete('/')
async def delete_user(username: str):
    return await delete_user_f(username)


@router.get('/users_all/da', response_class=HTMLResponse, name='users_all/da')
async def get_all_f_users(request: Request):
    print('hi get_all_f_users')

    users = await get_all_users()
    print(users)
    converted_users = [convert_record_to_user_patch(record) for record in users]
    print(converted_users)
    context = {
        'request': request,
        'users': users
    }
    return templates.TemplateResponse("users_all/da.html", context=context)


def convert_record_to_user_patch(record):
    return UserPatch(
        name=record.get('name'),
        surname=record.get('surname'),
        phone_number=record.get('phone_number'),
        email=record.get('email'),
        role=record.get('role')
    )
