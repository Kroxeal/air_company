from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from src.db.models import BaseDepartment, Department
from src.services.CRUD.Departments_crud import create_department, read_department, change_department, \
    change_department_partially, delete_department_f, get_all_departments_f

router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.post('/add', response_model=BaseDepartment)
async def create_department_endpoint(department: BaseDepartment):
    return await create_department(department)


@router.get('/get/{department_name}', response_model=BaseDepartment)
async def get_department(department_name: str):
    return await read_department(department_name)


@router.put('/put/{department_name}', response_model=BaseDepartment)
async def update_department(name: str, department: BaseDepartment):
    return await change_department(name, department)


@router.patch('/update/{department_name}', response_model=Department)
async def update_department_partially(request: Request, department_name: str, department: Department):
    print(department_name)
    print(department)
    result = await change_department_partially(department_name, department)
    context = {
        'request': request,
        'result': result,
    }
    print(context)
    return templates.TemplateResponse('department/update_department.html', context=context)


@router.delete('/delete/{department_name}')
async def delete_department(department_name: str):
    return await delete_department_f(department_name)


@router.get('/get_departments/all', response_model=BaseDepartment, name='get_departments/all')
async def get_all_department(request: Request):
    departments = await get_all_departments_f()
    result = [convert_record_to_department_patch(department) for department in departments]
    context = {
        'request': request,
        'departments': result,

    }
    print(context)
    return templates.TemplateResponse('department/departments_all.html', context=context)


def convert_record_to_department_patch(record):
    return BaseDepartment(
        name=record.get('name'),
        description=record.get('description'),
    )


@router.get('/edit_form/{department_name}')
async def edit_department(request: Request, department_name: str):
    context = {
        'request': request,
        'department_name': department_name,
    }
    print(context)
    return templates.TemplateResponse('department/update_department.html', context=context)


@router.get('/add_form')
async def add_department(request: Request):
    context = {
        'request': request,
    }
    print(context)
    print('add_form')
    return templates.TemplateResponse('department/add_department.html', context=context)
