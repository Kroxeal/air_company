import json

from fastapi import APIRouter, Request
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from src.db.models import Aircraft, PatchAircraft
from src.services.CRUD.Aircrafts_crud import create_aircraft_raw, get_aircraft_raw, update_aircraft_partially_raw, \
    delete_aircraft_raw, get_all_aircrafts_f, get_all_aircrafts_name_model_f

router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.post('/add', response_model=Aircraft)
async def crate_aircraft(aircraft: Aircraft):
    return await create_aircraft_raw(aircraft)


@router.get('/get/{model}', response_model=Aircraft)
async def get_aircraft(model: str):
    return await get_aircraft_raw(model)


@router.patch('/update/{registration_number}', response_model=PatchAircraft)
async def update_aircraft_partially(registration_number: str, aircraft: PatchAircraft):
    return await update_aircraft_partially_raw(registration_number, aircraft)


@router.delete('/delete/{registration_number}')
async def delete_aircraft(registration_number: str):
    return await delete_aircraft_raw(registration_number)


@router.get('/get_aircrafts/all', name='get_aircrafts/all')
async def get_aircraft(request: Request):
    result = await get_all_aircrafts_f()
    context = {
        'request': request,
        'aircrafts': result,
    }
    return templates.TemplateResponse('aircraft/aircrafts_all.html', context=context)


@router.get('/add_form')
async def add_aircraft_form(request: Request):
    context = {
        'request': request,
    }
    return templates.TemplateResponse('aircraft/add_aircraft.html', context=context)


@router.get('/edit_form/{registration_number}')
async def edit_aircraft_form(request: Request, registration_number: str):
    context = {
        'request': request,
        'registration_number': registration_number,
    }
    return templates.TemplateResponse('aircraft/update_aircraft.html', context=context)


@router.get('/get_models/all')
async def get_aircraft_models_f(request: Request):
    aircrafts = await get_all_aircrafts_name_model_f()
    context = {
        'aircraft': aircrafts,
    }
    return context
