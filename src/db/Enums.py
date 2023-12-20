from enum import Enum


class StatusUserRole(str, Enum):
    admin = "admin"
    user = "user"
    employee = "employee"


class StatusEmployeePosition(str, Enum):
    flight_attendant = "Flight Attendant"
    pilot = "Pilot"
    air_traffic_controller = "Air Traffic Controller"
    airport_security_officer = "Airport Security Officer"
    manager = "Manager"
    baggage_handler = "Baggage Handler"


class EmployeeStatus(str, Enum):
    active = "Active"
    on_leave = "On Leave"
    training = "Training"
    suspended = "Suspended"
    resigned = "Resigned"
    retired = "Retired"
    on_duty = "On Duty"
    on_call = "On Call"
    sick_leave = "Sick Leave"
    remote_work = "Remote Work"


class PassportSex(str, Enum):
    Male = 'male'
    Female = 'female'


class PaymentStatus(str, Enum):
    paid = "Paid"
    pending = "Pending"
    failed = "Failed"

