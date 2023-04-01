import datetime as dt
from typing import Callable, Protocol, TypedDict, final
from typing_extensions import TypeAlias, Unpack


class UserData(TypedDict, total=False):
    email: str
    first_name: str
    last_name: str
    date_of_birth: dt.datetime
    address: str
    job_title: str
    phone: str


@final
class RegistrationData(UserData, total=False):
    # special
    password: str
    password1: str
    password2: str


@final
class LoginData(TypedDict):
    username: str
    password: str


@final
class RegistrationDataFactory(Protocol):
    def __call__(
        self,
        **fields: Unpack[RegistrationData],
    ) -> RegistrationData:
        ...



UserAssertion: TypeAlias = Callable[[str, UserData], None]
