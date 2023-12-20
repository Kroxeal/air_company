import datetime
import decimal

from fastapi import UploadFile
from pydantic import BaseModel, UUID4, Field, model_validator
from datetime import date, timezone
import json

from typing_extensions import Optional

from src.db.Enums import StatusUserRole, StatusEmployeePosition, EmployeeStatus, PassportSex


class BaseUser(BaseModel):
    name: str
    surname: str
    phone_number: str
    email: str


class PostUser(BaseModel):
    username: str
    name: str
    surname: str
    phone_number: str
    email: str
    password: str
    role: StatusUserRole


class UserRegistration(BaseModel):
    username: str
    name: str
    surname: str
    phone_number: str
    email: str
    password: str


class BasePassport(BaseModel):
    passport_number: str
    nationality: str
    sex: str
    address: str
    date_of_birth: date
    date_of_issue: date
    date_of_expire: date


class BaseEmployee(BaseModel):
    position: str
    salary: decimal.Decimal
    department_id: UUID4 = None
    user_id: UUID4 = None
    status: str


class CreateEmployee(BaseModel):
    user: UUID4
    department: UUID4
    position: str
    salary: decimal.Decimal
    status: str


class Aircraft(BaseModel):
    name: str
    model: str
    year_manufacture: int
    seating_capacity: int
    max_range: int
    engine_type: str
    status: str
    last_service: date
    manufacture: str
    registration_number: str


class AircraftModel(BaseModel):
    name: str
    model: str
    id: UUID4


class PatchAircraft(BaseModel):
    name: str = None
    model: str = None
    year_manufacture: int = None
    seating_capacity: int = None
    max_range: int = None
    engine_type: str = None
    status: str = None
    last_service: date = None
    manufacture: str = None
    registration_number: str = None


class PostTicket(BaseModel):
    flight_id: UUID4
    user_id: UUID4
    departure_datetime: datetime.datetime
    arrival_airport: str
    arrival_datetime: datetime.datetime
    available_seats: str
    ticket_price: str
    aircraft: str


class Flight(BaseModel):
    flight_number: str
    departure_airport: str
    departure_datetime: datetime.datetime
    arrival_airport: str
    arrival_datetime: datetime.datetime
    available_seats: str
    ticket_price: str
    aircraft: str


class PatchFlight(BaseModel):
    flight_number: str = None
    departure_datetime: datetime.datetime = None
    arrival_datetime: datetime.datetime = None
    departure_airport: str = None
    arrival_airport: str = None
    available_seats: int = None
    ticket_price: float = None
    aircraft: str = None


class FlightAll(BaseModel):
    id: UUID4 = None
    flight_number: str
    departure_datetime: datetime.datetime
    arrival_datetime: datetime.datetime
    departure_airport: str
    arrival_airport: str
    available_seats: int
    ticket_price: float
    aircraft: str


class FlightStatistics(FlightAll):
    registration_number: str


class FlightModel(BaseModel):
    id: UUID4
    departure_datetime: datetime.datetime
    arrival_datetime: datetime.datetime
    departure_airport: str
    arrival_airport: str


class Ticket(BaseModel):
    service_class: str
    price: float
    status: str
    booking_date: datetime.datetime


class TicketDetails(BaseModel):
    flight_id: str
    user_id: str
    service_class: str
    price: float
    status: str
    booking_date: datetime.datetime


class TicketAll(BaseModel):
    id: UUID4
    flight: str
    user: str
    service_class: str
    price: float
    status: str
    booking_date: datetime.datetime


class TicketsCart(TicketAll):
    departure_datetime: datetime.datetime
    arrival_datetime: datetime.datetime


class TicketCreate(BaseModel):
    id: UUID4 = None
    flight: UUID4
    user: UUID4
    service_class: str
    price: float = None
    status: str
    booking_date: datetime.datetime = None


class PatchTicket(BaseModel):
    flight_number: str = None
    service_class: str = None
    price: float = None
    status: str = None
    booking_date: datetime.datetime = None


class CartTicket(BaseModel):
    id: UUID4 = None
    flight: str
    service_class: str
    price: float = None
    status: str = None
    booking_date: datetime.datetime = None


class TicketPatch(BaseModel):
    id: UUID4 = None
    flight: str = None
    user: str = None
    service_class: str = None
    price: float = None
    status: str = None
    booking_date: datetime.datetime = None


class CreatePassport(BaseModel):
    passport_number: str = None
    nationality: str = None
    sex: str = None
    address: str = None
    date_of_birth: date = None
    date_of_issue: date = None
    date_of_expire: date = None
    photo: str = None
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            print('dec')
            print({**json.loads(value)})
            return cls(**json.loads(value))
        return value


class User(BaseUser):
    username: str
    password: str
    role: str = None


class UserID(BaseUser):
    id: UUID4


class UserResponse(BaseUser):
    username: str


class UserPatch(BaseUser):
    name: str = None
    surname: str = None
    phone_number: str = None
    email: str = None
    role: str = None


class UserAll(BaseUser):
    name: str = None
    surname: str = None
    phone_number: str = None
    email: str = None
    role: str = None
    username: str


class UserForm(BaseModel):
    id: UUID4
    name: str
    surname: str


class BaseDepartment(BaseModel):
    name: str
    description: str


class DepartmentForm(BaseModel):
    id: UUID4
    name: str
    description: str


class Department(BaseDepartment):
    name: str = None
    description: str = None


class BaseDepartmentID(BaseDepartment):
    id: UUID4


class EmployeeDetails(BaseEmployee):
    department_id: str
    user_id: str


class PatchEmployee(BaseModel):
    position: str = None
    salary: decimal.Decimal = None
    status: str = None
    department_name: str = None


class EmployeeUsers(BaseModel):
    name: str
    surname: str
    position: str
    salary: decimal.Decimal
    status: str
    department: str
    username: str


class PassportUsername(BaseModel):
    user: UUID4
    passport_number: str
    nationality: str
    sex: PassportSex
    address: str
    date_of_birth: date
    date_of_issue: date
    date_of_expire: date

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            print('dec')
            print({**json.loads(value)})
            return cls(**json.loads(value))
        return value


class PassportForUser(BaseModel):
    user: str = None
    passport_number: str
    nationality: str
    sex: PassportSex
    address: str
    date_of_birth: date
    date_of_issue: date
    date_of_expire: date

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            print('dec')
            print({**json.loads(value)})
            return cls(**json.loads(value))
        return value


class PassportUser(UserAll, BasePassport):
    photo: str


class SearchFlight(BaseModel):
    departure_airport: str = None
    arrival_airport: str = None
    arrival_datetime: datetime.datetime = None
    departure_datetime: datetime.datetime = None


