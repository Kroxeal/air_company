from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/hi")
async def welcome(request: Request):
    return templates.TemplateResponse("users_all/welcome.html", {"request": request})
