from fastapi import APIRouter, Request, Depends
from starlette.templating import Jinja2Templates

from src.db.models import UserPatch
from src.services.auth.auth import get_current_admin

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/hi", name='welcome/hi')
async def welcome(request: Request):
    return templates.TemplateResponse("users_all/welcome.html", {"request": request})
