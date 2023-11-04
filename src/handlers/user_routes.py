from fastapi import APIRouter

from src.db.models import User, UserResponse, BaseUser, UserPatch
from src.services.CRUD.Users_crud import create_user, get_user, update_user, update_user_partially

router = APIRouter()


#, current_user: User = Depends(get_current_user)
@router.post("/", response_model=User)
async def create_user_endpoint(user: User):
    try:
        return await create_user(user)
    except Exception as e:
        return {"error": str(e)}


@router.get("/{username}", response_model=UserResponse)
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


@router.put("/{username}", response_model=BaseUser)
async def change_user(username: str, user: BaseUser):
    return await update_user(username, user)


@router.patch("/{username}", response_model=UserPatch)
async def update_user(username: str, user: UserPatch):
    return await update_user_partially(username, user)

