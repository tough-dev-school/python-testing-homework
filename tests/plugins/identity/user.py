from typing import Callable, Protocol, TypedDict, final

from typing_extensions import TypeAlias, Unpack

UserAssertion: TypeAlias = Callable[[str, 'UserData'], None]


class UserData(TypedDict, total=False):
    """Represents the simplified user data.

    This data is required to create a new user. It does not include
    ``password``, because it is very special in django. Importing this type
    is only allowed under ``if TYPE_CHECKING`` in tests.
    """

    email: str
    first_name: str
    last_name: str
    date_of_birth: str
    address: str
    job_title: str
    phone: str


@final
class RegistrationData(UserData, total=False):
    """Represents the registration data.

    This data is required to create a new user.
    """

    password1: str
    password2: str


@final
class RegistrationDataFactory(Protocol):  # type: ignore[misc]
    """User data factory protocol."""

    def __call__(
        self,
        **fields: Unpack[RegistrationData],
    ) -> RegistrationData:
        """Creates the user data."""
