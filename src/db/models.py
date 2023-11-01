from pydantic import BaseModel, UUID4, Field
from datetime import date


class Aircraft(BaseModel):
    name: str
    model: str
    year_manufacturer: int
    seating_capacity: int
    max_range: int
    engine_type: str
    status: str
    last_service: str
    manufacturer: str


class Flight(BaseModel):
    flight_number: int
    departure_datetime: str
    arrival_datetime: str
    departure_airport: str
    arrival_airport: str
    available_seats: int
    ticket_price: float
    aircraft_id: UUID4


class Ticket(BaseModel):
    flight_id: UUID4
    user_id: UUID4
    service_class: str
    price: float
    status: str
    booking_date: str


class Passport(BaseModel):
    passport_number: str
    nationality: str
    sex: str
    address: str
    date_of_birth: str
    date_of_issue: str
    date_of_expire: str
    photo: bytes


class User(BaseModel):
    username: str
    name: str
    surname: str
    phone_number: str
    email: str
    password: str


class UserResponse(BaseModel):
    username: str
    name: str
    surname: str
    phone_number: str
    email: str

