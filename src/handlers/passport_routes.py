from datetime import date

from fastapi import APIRouter, Depends, Request, UploadFile, File, Form, Body
from starlette.templating import Jinja2Templates

from src.db.models import CreatePassport, BasePassport, User, PassportUsername
from src.services.CRUD.Passports_crud import create_passport, get_passport, get_passport_by_id, update_passport, \
    update_current_passport_partially, delete_passport_f, get_all_passports_f
from src.services.CRUD.Users_crud import get_user_with_id
from src.services.auth.auth import get_current_user
from src.services.image_service import save_file

router = APIRouter()
templates = Jinja2Templates(directory='templates')

# route_photo = await save_file(file)
#     print('hi')
#     passport.photo = route_photo
#     print(passport)
#     , file: UploadFile = File(...)


@router.post("/post/pas")
async def create_passport_endpoint(passport: PassportUsername = Body(...), uploaded_file: UploadFile = File(...)):
    print('hell')
    route_photo = await save_file(uploaded_file)
    created_passport = await create_passport(passport, route_photo.get('filename'))
    print(created_passport)

    context = {
        'passport': created_passport,
        'filename': uploaded_file.filename,
    }

    return context


@router.post("/post_image/all")
async def endpoxint(request: Request, uploaded_file: UploadFile = File(...)):
    print('hell')
    route_photo = await save_file(uploaded_file)
    print('hi')

    context = {
        'route': route_photo
    }

    return context


@router.post("/post_by_user", response_model=BasePassport)
async def create_passport_endpoint(passport: BasePassport, current_user: User = Depends(get_current_user)):
    try:
        username = current_user['sub']
        user = await get_user_with_id(username)
        user_id = user.id
        created_passport = await create_passport(user_id, passport)
        return created_passport
    except Exception as e:
        return {"error": str(e)}


@router.get("/get/{passport_number}", response_model=CreatePassport)
async def read_passport(passport_number: str):
    passport = await get_passport(passport_number)
    return passport


@router.get("/get/{username}", response_model=BasePassport)
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


@router.put("/put/{username}", response_model=CreatePassport)
async def change_all_current_passport(passport: CreatePassport, current_user: User = Depends(get_current_user)):
    username = current_user['sub']
    result = await update_passport(username, passport)
    return result


@router.patch("/patch/{username}", response_model=CreatePassport)
async def update_partially_passport(passport: CreatePassport, current_user: User = Depends(get_current_user)):
    username = current_user['sub']
    result = await update_current_passport_partially(username, passport)
    return result


@router.patch("/update/{passport_number}")
async def update_partially_passport(
        passport_number: str,
        passport: CreatePassport = Body(...),
        uploaded_file: UploadFile = File(...)
):
    route_photo = await save_file(uploaded_file)
    result = await update_current_passport_partially(passport_number, passport, route_photo.get('filename'))
    return result


@router.delete('/delete/{passport_number}')
async def delete_passport(passport_number: str):
    return await delete_passport_f(passport_number)


@router.get('/get_passports/all', name='get_passports/all')
async def get_all_passport(request: Request):
    result = await get_all_passports_f()
    context = {
        'request': request,
        'passports': result
    }
    print(context)
    return templates.TemplateResponse('passport/passports_all.html', context=context)


@router.get('/add_form')
async def add_passport_form(request: Request):
    context = {
        'request': request,
    }
    print(context)
    return templates.TemplateResponse('passport/add_passport.html', context=context)


@router.get('/edit_form/{passport_number}')
async def edit_department(request: Request, passport_number: str):
    context = {
        'request': request,
        'department_name': passport_number,
    }
    print(context)
    return templates.TemplateResponse('passport/update_passport.html', context=context)
