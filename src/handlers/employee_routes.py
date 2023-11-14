from fastapi import APIRouter

from src.db.models import BaseEmployee, EmployeeDetails, PatchEmployee, CreateEmployee
from src.services.CRUD.Employees_crud import create_employee, get_employee, get_employee_with_details, \
    update_employee_put, update_employee_partially_patch, delete_employee_f

router = APIRouter()


@router.post('/', response_model=CreateEmployee)
async def create_employee_by_username_department(
        username: str,
        department_name: str,
        employee: CreateEmployee):
    try:
        return await create_employee(username, department_name, employee)
    except Exception as e:
        return {'error': str(e)}


@router.get('/{username}', response_model=BaseEmployee)
async def get_employee_by_username(username: str):
    try:
        return await get_employee(username)
    except Exception as e:
        return {'error': str(e)}


@router.get('/detail/{username}', response_model=EmployeeDetails)
async def get_employee_by_username_with_detail(username: str):
    return await get_employee_with_details(username)


@router.put('/', response_model=BaseEmployee)
async def update_employee(username: str, employee: BaseEmployee):
    return await update_employee_put(username, employee)


@router.patch('/', response_model=PatchEmployee)
async def update_employee_partially(username: str, employee: PatchEmployee):
    return await update_employee_partially_patch(username, employee)


@router.delete('/')
async def delete_employee(username: str):
    return await delete_employee_f(username)

