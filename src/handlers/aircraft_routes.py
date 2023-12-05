from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

from src.db.models import Aircraft, PatchAircraft
from src.services.CRUD.Aircrafts_crud import create_aircraft_raw, get_aircraft_raw, update_aircraft_partially_raw, \
    delete_aircraft_raw, get_all_aircrafts_f

router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.post('/post', response_model=Aircraft)
async def crate_aircraft(aircraft: Aircraft):
    return await create_aircraft_raw(aircraft)


@router.get('/get/{model}', response_model=Aircraft)
async def get_aircraft(model: str):
    return await get_aircraft_raw(model)


@router.patch('/patch', response_model=PatchAircraft)
async def update_aircraft_partially(model: str, aircraft: PatchAircraft):
    return await update_aircraft_partially_raw(model, aircraft)


@router.delete('/delete/{model}')
async def delete_aircraft(model: str):
    return await delete_aircraft_raw(model)


@router.get('/get_aircrafts/all', name='get_aircrafts/all')
async def get_aircraft(request: Request):
    result = await get_all_aircrafts_f()
    context = {
        'request': request,
        'aircrafts': result,
    }
    return templates.TemplateResponse('aircraft/aircrafts_all.html', context=context)

