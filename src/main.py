from fastapi import FastAPI, Depends

from src.db.models import User
from src.services.auth.auth import get_current_user
from src.services.auth.auth_routes import router as auth_routes
from src.handlers.user_routes import router as user_routes
from src.handlers.passport_routes import router as passport_router

import pdb

app = FastAPI()

app.include_router(user_routes, prefix='/user', tags=['Users'])
app.include_router(auth_routes, prefix='/auth', tags=['Auth'])
app.include_router(passport_router, prefix='/passport', tags=['Passports'])


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
