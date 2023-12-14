import datetime

from fastapi import APIRouter, Request
from pydantic import UUID4
from starlette.templating import Jinja2Templates

from src.db.models import Ticket, TicketDetails, PatchTicket, TicketAll, TicketCreate, TicketPatch
from src.services.CRUD.Flights_crud import select_price
from src.services.CRUD.Tickets_crud import create_ticket_raw, get_ticket_raw, get_ticket_details_raw, update_ticket_raw, \
    delete_ticket_raw, get_all_tickets, update_ticket_form_raw
from src.services.logic import logic_ticket


router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.post('/add')
async def create_ticket(ticket: TicketCreate):
    ticket.booking_date = datetime.datetime.now()
    price = await select_price(ticket.flight)
    price = price.get('ticket_price')
    ticket.price = logic_ticket.add_sum_by_status(ticket.service_class, price)
    ticket = await create_ticket_raw(ticket)
    context = {
        'ticket': ticket
    }
    return context


@router.get('/get', response_model=Ticket)
async def get_ticket(username: str, flight_number: str):
    return await get_ticket_raw(username, flight_number)


@router.get('/detail/', response_model=TicketDetails)
async def get_ticket_details(username: str, flight_number: str):
    return await get_ticket_details_raw(username, flight_number)


@router.patch('/update/{id}')
async def update_ticket_form(id: str, ticket: TicketPatch):
    ticket = await update_ticket_form_raw(id, ticket)
    context = {
        'ticket': ticket,
    }
    return context


@router.patch('/patch', response_model=PatchTicket)
async def update_ticket(username: str, flight_number: str, ticket: PatchTicket):
    return await update_ticket_raw(username, flight_number, ticket)


@router.delete('/delete/{id}')
async def delete_ticket(id: UUID4):
    return await delete_ticket_raw(id)


@router.get('/get_tickets/all', name='get_tickets/all')
async def get_all_tickets_form(request: Request):
    results = await get_all_tickets()
    context = {
        'request': request,
        'tickets': results
    }
    return templates.TemplateResponse('ticket/tickets_all.html', context=context)


@router.get('/add_form')
async def get_all_tickets_form(request: Request):
    context = {
        'request': request,
    }
    return templates.TemplateResponse('ticket/add_ticket.html', context=context)


@router.get('/edit_form/{id}')
async def edit_ticket_form(id: str, request: Request):
    context = {
        'request': request,
        'id': id,
    }
    return templates.TemplateResponse('ticket/update_ticket.html', context=context)

