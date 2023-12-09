from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

from src.db.models import Flight, PatchFlight
from src.services.CRUD.Flights_crud import create_flight_raw, get_flight_raw, update_flight_partially_raw, \
    delete_flight_raw, get_all_flight_raw, get_all_flight_form

router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.post('/add')
async def create_flight(requset: Request, flight: Flight):
    result = await create_flight_raw(flight)
    context = {
        'flight': result,
    }
    return context


@router.get('/get/{flight_number}', response_model=Flight)
async def get_flight(flight_number: str):
    return await get_flight_raw(flight_number)


@router.patch('/update/{flight_number}', response_model=PatchFlight)
async def update_flight_partially(flight_number: str, flight: PatchFlight):
    return await update_flight_partially_raw(flight_number, flight)


@router.delete('/delete/{flight_number}')
async def delete_flight(flight_number: str):
    return await delete_flight_raw(flight_number)


@router.get('/get_flights/all', name='get_flights/all')
async def get_all_flight(request: Request):
    result = await get_all_flight_raw()
    context = {
        'request': request,
        'flights': result,
    }
    return templates.TemplateResponse('flight/flights_all.html', context=context)


@router.get('/add_form')
async def get_add_flight(request: Request):
    context = {
        'request': request,
    }
    return templates.TemplateResponse('flight/add_flight.html', context=context)


@router.get('/edit_form/{flight_number}')
async def get_edit_flight_form(request: Request, flight_number: str):
    context = {
        'request': request,
        'flight_number': flight_number,
    }
    return templates.TemplateResponse('flight/update_flight.html', context=context)


@router.get('/get_flights_form/all')
async def get_flights_form():
    flights = await get_all_flight_form()
    context = {
        'flight': flights,
    }
    return context
