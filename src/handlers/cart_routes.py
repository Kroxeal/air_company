import datetime

from fastapi import APIRouter, Request, Depends
from starlette.templating import Jinja2Templates

from src.db.models import UserPatch, CartTicket
from src.services.CRUD.Flights_crud import select_price
from src.services.auth.auth import get_current_user
from src.services.cart.cart_db import get_all_tickets_user, update_ticket_raw
from src.services.logic import logic_ticket

router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.get('/all_tickets')
async def get_all_tickets(current_user: UserPatch = Depends(get_current_user)):
    username = current_user.get('sub')
    result = await get_all_tickets_user(username)
    print(result)
    return result


@router.get('/all_tickets/form', name='all_tickets/form')
async def get_all_tickets(request: Request, current_user: UserPatch = Depends(get_current_user)):
    username = current_user.get('sub')
    tickets = await get_all_tickets_user(username)
    print(tickets)
    context = {
        'request': request,
        'tickets': tickets,
    }
    return templates.TemplateResponse('cart/show_cart.html', context=context)


@router.get('/edit_form/{id}')
async def edit_ticket_form(id: str, request: Request):
    context = {
        'request': request,
        'id': id,
    }
    return templates.TemplateResponse('cart/update_cart.html', context=context)


@router.patch('/update_ticket/{id}')
async def update_ticket(id: str, ticket: CartTicket):
    ticket.id = id
    ticket.booking_date = datetime.datetime.now()
    price = await select_price(ticket.flight)
    price = price.get('ticket_price')
    ticket.price = logic_ticket.add_sum_by_status(ticket.service_class, price)
    ticket.status = 'paid'
    result = await update_ticket_raw(ticket)
    return result

