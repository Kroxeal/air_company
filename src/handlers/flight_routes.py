from fastapi import APIRouter

from src.db.models import Flight, PatchFlight
from src.services.CRUD.Flights_crud import create_flight_raw, get_flight_raw, update_flight_partially_raw, \
    delete_flight_raw

router = APIRouter()


@router.post('/', response_model=Flight)
async def create_flight(model: str, flight: Flight):
    return await create_flight_raw(model, flight)


@router.get('/{flight_number}', response_model=Flight)
async def get_flight(flight_number: str):
    return await get_flight_raw(flight_number)


@router.patch('/{}flight_number', response_model=PatchFlight)
async def update_flight_partially(flight_number: str, flight: PatchFlight):
    return await update_flight_partially_raw(flight_number, flight)


@router.delete('{flight_number}')
async def delete_flight(flight_number: str):
    return await delete_flight_raw(flight_number)
