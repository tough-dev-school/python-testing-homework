import datetime as dt
from typing import Callable, Optional, TypedDict, final

from typing_extensions import TypeAlias


@final
class RegistrationData(TypedDict, total=False):
    """Represent the user data that is required to create a new user."""
    email: str
    first_name: str
    last_name: str
    date_of_birth: dt.datetime
    address: str
    job_title: str
    phone: str
    phone_type: int
    password: str
    password1: Optional[str]
    password2: Optional[str]

UserAssertion: TypeAlias = Callable[[RegistrationData], None]
