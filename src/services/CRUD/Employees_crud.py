from fastapi import HTTPException

from src.db.models import BaseEmployee, EmployeeDetails, PatchEmployee, CreateEmployee, EmployeeUsers
from src.db.settings import database
from src.services.decorators.connect_decorator import db_connection


@db_connection
async def create_employee(employee: CreateEmployee):
    query_params = """
    INSERT INTO employees(
    position,
    salary,
    status,
    department_id,
    user_id
    )
    VALUES (
        $1,
        $2,
        $3,
        $4,
        $5
    )
    """
    values = (
        employee.position,
        employee.salary,
        employee.status,
        employee.department,
        employee.user,
    )
    result = await database.execute(query_params, *values)
    print(result)
    return employee


@db_connection
async def get_employee(username: str):
    insert_query = """
    SELECT * FROM employees
    WHERE user_id = (
    SELECT id FROM employees WHERE username = $1
    )
    """
    values = (
        username,
    )
    result = await database.fetchrow(insert_query, *values)
    if result:
        employee = BaseEmployee(**result)
        return employee
    else:
        raise HTTPException(status_code=400, detail="There's no such a Employee")


@db_connection
async def get_employee_with_details(username: str):
    query = """
        SELECT 
        Employees.*,
        Users.username,
        Departments.name AS department_name
        FROM Employees
        LEFT JOIN Users ON Employees.user_id = Users.id
        LEFT JOIN Departments ON Employees.department_id = Departments.id
        WHERE Users.username = $1
    """
    result = await database.fetchrow(query, username)
    if result:
        employee_data = {
            "position": result["position"],
            "salary": result["salary"],
            "department_id": result["department_name"],
            "user_id": result["username"],
            "status": result["status"],
        }
        employee = EmployeeDetails(**employee_data)
        return employee
    else:
        raise HTTPException(status_code=400, detail="There's no such an Employee")


@db_connection
async def update_employee_put(username, employee: BaseEmployee):
    query = """
    UPDATE Employees
    SET
    position = $1,
    salary = $2,
    status = $3,
    department_id = $4
    WHERE user_id = (
        SELECT id FROM Users WHERE username = $5
    )
    """
    values = (
        employee.position,
        employee.salary,
        employee.status,
        employee.department_id,
        username,
    )
    await database.execute(query, *values)
    return employee


@db_connection
async def update_employee_partially_patch(username: str, employee: PatchEmployee):
    query = """
    UPDATE employees
    SET
    position = COALESCE($1, position),
    salary = COALESCE($2, salary),
    status = COALESCE($3, status),
    department_id = COALESCE((SELECT id FROM departments WHERE name = $4), department_id)
    WHERE
    user_id = (SELECT id FROM users WHERE username = $5);
    """
    values = (
        employee.position,
        employee.salary,
        employee.status,
        employee.department_name,
        username,
    )
    await database.execute(query, *values)
    return employee


@db_connection
async def delete_employee_f(username: str):
    query = '''
    DELETE FROM employees
    WHERE user_id = (
    SELECT id FROM users WHERE username = $1
    )
    '''
    values = (
        username,
    )
    await database.execute(query, *values)
    return f'Employee {username} deleted'


@db_connection
async def if_user_is_employee(username: str):
    print('hello')
    query = '''
    SELECT position, salary, status
    FROM employees
    LEFT JOIN Users ON employees.user_id = users.id
    WHERE Users.username = $1
    '''
    values = (
        username,
    )
    print(query)
    print(values)
    result = await database.fetchrow(query, *values)
    print(result)
    if result:
        return PatchEmployee(**result)
    else:
        raise HTTPException(status_code=400, detail="There's no such an Employee")


@db_connection
async def get_all_employees():
    print('enter get_all_employees crud')

    query = '''
    SELECT
        users.name, users.surname, users.username,
        employees.*, departments.name as department_name
        
    FROM Employees
    INNER JOIN Users ON Employees.user_id = users.id
    INNER JOIN Departments ON Employees.department_id = departments.id
    '''
    result = await database.fetchall(query)
    print({"result": result})
    employee_data_list = []
    for row in result:
        employee_data = {
            "name": row["name"],
            "surname": row["surname"],
            "position": row["position"],
            "salary": row["salary"],
            "status": row["status"],
            "department": row["department_name"],
            "username": row["username"],
        }
        employee_data_list.append(EmployeeUsers(**employee_data))

    return employee_data_list
