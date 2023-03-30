from datetime import datetime
from typing import TypedDict, final


@final
class UserData(TypedDict):
    first_name: str
    last_name: str
    date_of_birth: datetime
    address: str
    job_title: str
    phone: str
    phone_type: int


class RegistrationData(TypedDict):
    email: str
    password1: str
    password2: str
