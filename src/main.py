from fastapi import FastAPI, Depends

from src.db.models import User
from src.services.auth.auth import get_current_user
from src.services.auth.auth_routes import router as auth_routes
from src.handlers.user_routes import router as user_routes
from src.handlers.passport_routes import router as passport_router
from src.handlers.department_routes import router as department_routes
from src.handlers.employee_routes import router as employee_routes
from src.handlers.aircraft_routes import router as aircraft_routes
from src.handlers.flight_routes import router as flight_routes
from src.handlers.ticket_routes import router as ticket_router

import pdb

app = FastAPI()

app.include_router(user_routes, prefix='/user', tags=['Users'])
app.include_router(auth_routes, prefix='/auth', tags=['Auth'])
app.include_router(passport_router, prefix='/passport', tags=['Passports'])
app.include_router(department_routes, prefix='/department', tags=['Departments'])
app.include_router(employee_routes, prefix='/employee', tags=['Employees'])
app.include_router(aircraft_routes, prefix='/aircraft', tags=['Aircrafts'])
app.include_router(flight_routes, prefix='/flight', tags=['Flights'])
app.include_router(ticket_router, prefix='/ticket', tags=['Tickets'])


@app.get("/secure-data")
async def get_secure_data(current_user: User = Depends(get_current_user)):
    # В этом роуте, только аутентифицированные пользователи могут получить доступ
    return {"message": "This is secure data"}


# @app.get("/protected")
# async def protected_route(token: str = Depends(oauth2_scheme)):
#     payload = decode_access_token(token)
#     return {"message": "Защищенный маршрут", "username": payload.get("username")}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)
