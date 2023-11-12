from src.db.models import BaseDepartment, Department
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
    query_params = [name]
    update_columns = []
    print(department.name)
    print(department.description)

    if department.name is not None:
        query_params.append(department.name)
        update_columns.append("name = $2")

    if department.description is not None:
        query_params.append(department.description)
        update_columns.append("description = $3")

    update_query = f"""
    UPDATE departments
    SET {', '.join(update_columns)}
    WHERE name = $1
    """
    print(update_query)
    print(*query_params)

    result = await database.execute(update_query, *query_params)
    print(result)
    updated_department = await database.fetchrow(
        "SELECT * FROM departments WHERE name = $1",
        department.name
    )
    print(updated_department)

    return Department(**updated_department)
