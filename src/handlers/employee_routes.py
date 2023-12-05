from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from src.db.models import BaseEmployee, EmployeeDetails, PatchEmployee, CreateEmployee, EmployeeUsers
from src.services.CRUD.Employees_crud import create_employee, get_employee, get_employee_with_details, \
    update_employee_put, update_employee_partially_patch, delete_employee_f, if_user_is_employee, get_all_employees

router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.post('/post')
async def create_employee_by_username_department(
        request: Request,
        employee: CreateEmployee):
    print(employee)
    result = await create_employee(employee)
    print(result)
    context = {
        'request': request,
        'employee': result
    }
    return templates.TemplateResponse('employee/add_employee.html', context=context)


@router.get('/get/{username}', response_model=BaseEmployee)
async def get_employee_by_username(username: str):
    try:
        return await get_employee(username)
    except Exception as e:
        return {'error': str(e)}


@router.get('/detail/{username}', response_model=EmployeeDetails)
async def get_employee_by_username_with_detail(username: str):
    return await get_employee_with_details(username)


@router.put('/put', response_model=BaseEmployee)
async def update_employee(username: str, employee: BaseEmployee):
    return await update_employee_put(username, employee)


@router.patch('/update/{username}', response_model=PatchEmployee)
async def update_employee_partially(request: Request, username: str, employee: PatchEmployee):
    result = await update_employee_partially_patch(username, employee)
    context = {
        'request': request,
        'employee': result,
    }
    return templates.TemplateResponse('/employee/update_employee.html', context=context)


@router.delete('/delete/{username}')
async def delete_employee(username: str):
    return await delete_employee_f(username)


@router.get('/isemployee/{username}', response_model=PatchEmployee)
async def is_employee(username: str):
    return await if_user_is_employee(username)


@router.get('/employees_all', response_class=HTMLResponse, name='get_employees/all')
async def all_employees(request: Request):
    print('enter all_employees')
    employees = await get_all_employees()
    print(employees)
    context = {
        'request': request,
        'employees': employees,
    }
    return templates.TemplateResponse('employee/employees_all.html', context=context)


@router.get('/add_form')
async def add_employee(request: Request):
    context = {
        'request': request,
    }
    return templates.TemplateResponse('employee/add_employee.html', context=context)


@router.get('/edit_form/{username}')
async def edit_employee(request: Request):
    context = {
        'request': request,
    }
    return templates.TemplateResponse('employee/update_employee.html', context=context)
