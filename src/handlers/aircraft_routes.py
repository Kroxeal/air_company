from fastapi import APIRouter

from src.db.models import Aircraft, PatchAircraft
from src.services.CRUD.Aircrafts_crud import create_aircraft_raw, get_aircraft_raw, update_aircraft_partially_raw, \
    delete_aircraft_raw

router = APIRouter()


@router.post('/', response_model=Aircraft)
async def crate_aircraft(aircraft: Aircraft):
    return await create_aircraft_raw(aircraft)


@router.get('/{model}', response_model=Aircraft)
async def get_aircraft(model: str):
    return await get_aircraft_raw(model)


@router.patch('/', response_model=PatchAircraft)
async def update_aircraft_partially(model: str, aircraft: PatchAircraft):
    return await update_aircraft_partially_raw(model, aircraft)


@router.delete('/{model}')
async def delete_aircraft(model: str):
    return await delete_aircraft_raw(model)
