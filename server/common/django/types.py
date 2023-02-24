"""
This file is only required for better typing.

Most of the things here are fixes / missing features in `django-stubs`.
It is better to have links for open bug reports / feature requests
near each type, so we can easily track them and refactor
our code when new versions are released.
"""

from typing import Protocol


# TODO: bug in django-stubs with settings
class Settings(Protocol):
    """Our plugin cannot resolve some settings during type checking."""

    PLACEHOLDER_API_URL: str
    PLACEHOLDER_API_TIMEOUT: int
