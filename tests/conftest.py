"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""

from datetime import date, timedelta

import pytest
from mimesis import Address, Person

person = Person()
address = Address()

pytestmark = pytest.mark.django_db

DAYS_IN_YEAR = 365


pytest_plugins = [
    # Should be the first custom one:
    'plugins.django_settings',

    # TODO: add your own plugins here!
]


@pytest.fixture()
def user_data() -> dict[str, object]:
    """Generate random user data fixture."""
    age = person.age()
    birthdate = date.today() - timedelta(days=age * DAYS_IN_YEAR)

    return {
        'email': person.email(),
        'password': person.password(),
        'first_name': person.first_name(),
        'last_name': person.last_name(),
        'date_of_birth': birthdate,
        'address': address.address(),
        'job_title': person.occupation(),
        'phone': person.telephone(),
    }
