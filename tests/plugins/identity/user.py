import datetime as dt
from typing import Callable, TypeAlias, TypedDict
from typing import Protocol, Unpack, final


@final
class UserData(TypedDict, total=False):
    """
    Represent the user data that is required to create a new user.
    Does not include `password`, because it's special field in Django.
    """
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
    """Represent the user data that is required to create a new user."""
    password_first: str
    password_second: str


@final
class RegistrationDataFactory(Protocol):
    """User data factory protocol."""
    def __call__(self, **fields: Unpack[RegistrationData]) -> RegistrationData:
        """User data factory protocol."""
