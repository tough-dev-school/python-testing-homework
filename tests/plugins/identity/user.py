import datetime as dt
from typing import TypedDict, TypeAlias, Callable
from typing import final, Protocol, Unpack


@final
class UserData(TypedDict, total=False):
    email: str
    first_name: str
    last_name: str
    date_of_birth: dt.datetime
    address: str
    job_title: str
    phone: str
    lead_id: int
    is_staff: bool
    is_active: bool


UserAssertion: TypeAlias = Callable[[str, UserData], None]


@final
class RegistrationData(UserData, total=False):
    password_first: str
    password_second: str


@final
class RegistrationDataFactory(Protocol):
    def __call__(self, **fields: Unpack[RegistrationData]) -> RegistrationData:
        """User data factory protocol."""
