import pytest
from mimesis.locales import Locale
from mimesis.schema import Field


@pytest.fixture()
def mfield(faker_seed: int):
    """Get seeded and localed mimesis field."""
    return Field(locale=Locale.EN, seed=faker_seed)
