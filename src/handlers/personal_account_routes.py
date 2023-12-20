from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter
templates = Jinja2Templates(directory='templates')


@router.get('/get_form')
async def get_form(request: Request):
    context = {
        'request': request,
    }
    return templates.TemplateResponse('personal_account/account.html', context=context)
