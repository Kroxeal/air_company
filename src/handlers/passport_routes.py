from fastapi import APIRouter, Depends
from pydantic import UUID4

from src.db.models import CreatePassport, BasePassport, User
from src.services.CRUD.Passports_crud import create_passport, get_passport, get_passport_by_id, update_passport, \
    update_current_passport_partially
from src.services.CRUD.Users_crud import get_user, get_user_with_id
from src.services.auth.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=BasePassport)
async def create_passport_endpoint(passport: BasePassport, current_user: User = Depends(get_current_user)):
    try:
        username = current_user['sub']
        user = await get_user_with_id(username)
        user_id = user.id
        created_passport = await create_passport(user_id, passport)
        return created_passport
    except Exception as e:
        return {"error": str(e)}


@router.get("/{passport_number}", response_model=CreatePassport)
async def read_passport(passport_number: str):
    passport = await get_passport(passport_number)
    return passport


@router.get("/", response_model=BasePassport)
async def get_current_passport(current_user: User = Depends(get_current_user)):
    try:
        username = current_user['sub']
        user = await get_user_with_id(username)
        user_id = user.id
        current_passport = await get_passport_by_id(user_id)
        print(current_passport)
        return current_passport
    except Exception as e:
        return {"error": str(e)}


@router.put("/", response_model=CreatePassport)
async def change_all_current_passport(passport: CreatePassport, current_user: User = Depends(get_current_user)):
    username = current_user['sub']
    user = await get_user_with_id(username)
    user_id = user.id
    result = await update_passport(user_id, passport)
    return result


@router.patch("/", response_model=CreatePassport)
async def update_partially_passport(passport: CreatePassport, current_user: User = Depends(get_current_user)):
    username = current_user['sub']
    user = await get_user_with_id(username)
    user_id = user.id
    result = await update_current_passport_partially(user_id, passport)
    return result

