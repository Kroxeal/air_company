from src.db.models import BaseDepartment, Department, BaseDepartmentID
from src.db.settings import database
from src.services.decorators.connect_decorator import db_connection


@db_connection
async def create_department(department: BaseDepartment):
    insert_query = """
    INSERT INTO departments (
    name, 
    description
    )
    VALUES ($1, $2)
    """
    values = (
        department.name,
        department.description,
    )
    await database.execute(insert_query, *values)

    return department


@db_connection
async def read_department(department_name: str):
    isert_query = """
    SELECT * FROM departments
    WHERE name = $1
    """
    result = await database.fetchrow(isert_query, department_name)
    department = BaseDepartment(**result)
    return department


@db_connection
async def get_department_with_id(department_name: str):
    isert_query = """
        SELECT * FROM departments
        WHERE name = $1
        """
    result = await database.fetchrow(isert_query, department_name)
    department = BaseDepartmentID(**result)
    return department


@db_connection
async def change_department(name: str, department: BaseDepartment):
    isert_query = """
    UPDATE departments 
    SET
    name = $1,
    description = $2
    WHERE name = $3
    """
    values = (
        department.name,
        department.description,
        name,
    )

    await database.execute(isert_query, *values)
    return department


@db_connection
async def change_department_partially(name: str, department: Department):
    query = """
    UPDATE departments
    SET
    name = COALESCE($1, name),
    description = COALESCE($2, description)
    WHERE name = $3
    """
    values = (
        department.name,
        department.description,
        name,
    )
    await database.execute(query, *values)
    return department


@db_connection
async def delete_department_f(department_name: str):
    query = '''
    DELETE FROM departments
    WHERE name = $1
    '''
    values = (
        department_name,
    )
    await database.execute(query, *values)
    return f'Department {department_name} deleted'
