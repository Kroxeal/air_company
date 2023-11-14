import decimal

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


class BaseEmployee(BaseModel):
    position: str
    salary: decimal.Decimal
    department_id: UUID4 = None
    user_id: UUID4 = None
    status: str


class CreateEmployee(BaseModel):
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
