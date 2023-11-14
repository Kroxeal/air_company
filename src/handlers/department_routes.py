from fastapi import APIRouter

from src.db.models import BaseDepartment, Department
from src.services.CRUD.Departments_crud import create_department, read_department, change_department, \
    change_department_partially, delete_department_f

router = APIRouter()


@router.post('/', response_model=BaseDepartment)
async def create_department_endpoint(department: BaseDepartment):
    return await create_department(department)


@router.get('/{department_name}', response_model=BaseDepartment)
async def get_department(department_name: str):
    return await read_department(department_name)


@router.put('/{department_name}', response_model=BaseDepartment)
async def update_department(name: str, department: BaseDepartment):
    return await change_department(name, department)


@router.patch('/{department_name}', response_model=BaseDepartment)
async def update_department_partially(name: str, department: Department):
    return await change_department_partially(name, department)


@router.delete('/')
async def delete_department(department_name: str):
    return await delete_department_f(department_name)
