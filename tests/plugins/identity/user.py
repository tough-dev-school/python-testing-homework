import datetime as dt
from typing import TypedDict, final


class UserData(TypedDict, total=False):
    first_name: str
    last_name: str
    date_of_birth: dt.datetime
    address: str
    job_title: str
    phone: str
    phone_type: int


@final
class RegistrationData(UserData, total=False):
    password1: str
    password2: str
