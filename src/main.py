from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

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
from src.handlers.login_routes import router as login_routes
from src.handlers.welcome import router as welcome_routes
from src.handlers.handlers_analytics_queries.flight_popularity_routes import router as analytics_routes
from src.handlers.cart_routes import router as cart_routes
from src.handlers.handlers_statistics.flight_statistic_routes import router as statistics_routes


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
app.include_router(login_routes, prefix='/login', tags=['Login'])
app.include_router(welcome_routes, prefix='/welcome', tags=['Welcome'])
app.include_router(analytics_routes, prefix='/analytics', tags=['Analytics'])
app.include_router(cart_routes, prefix='/cart', tags=['Cart'])
app.include_router(statistics_routes, prefix='/statistics', tags=['Statistics'])

app.mount("/welcome/assets", StaticFiles(directory="static"), name="static")
app.mount("/static", StaticFiles(directory="static"), name="static")


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/secure-data")
async def get_secure_data(current_user: User = Depends(get_current_user)):
    return {"message": "This is secure data"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)
