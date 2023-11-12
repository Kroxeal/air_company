from pydantic import BaseModel, UUID4, Field
from datetime import date


class BaseUser(BaseModel):
    name: str
    surname: str
    phone_number: str
    email: str


class BasePassport(BaseModel):
    passport_number: str
    nationality: str
    sex: str
    address: str
    date_of_birth: date
    date_of_issue: date
    date_of_expire: date


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


class CreatePassport(BasePassport):
    passport_number: str = None
    nationality: str = None
    sex: str = None
    address: str = None
    date_of_birth: date = None
    date_of_issue: date = None
    date_of_expire: date = None
    photo: bytes = None


class User(BaseUser):
    username: str
    password: str


class UserID(BaseUser):
    id: UUID4


class UserResponse(BaseUser):
    username: str


class UserPatch(BaseUser):
    name: str = None
    surname: str = None
    phone_number: str = None
    email: str = None


class BaseDepartment(BaseModel):
    name: str
    description: str


class Department(BaseDepartment):
    name: str = None
    description: str = None