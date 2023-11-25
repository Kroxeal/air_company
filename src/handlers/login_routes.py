from fastapi import FastAPI, Request, Depends, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Подключаем шаблонизатор Jinja2
templates = Jinja2Templates(directory="templates")


# Ваш метод для входа на страницу авторизации
@router.get("/auth", response_class=HTMLResponse)
async def login_page(request: Request):
    # Вместо "login.html" укажите имя вашего HTML-файла
    return templates.TemplateResponse("auth/user.html", {"request": request})
