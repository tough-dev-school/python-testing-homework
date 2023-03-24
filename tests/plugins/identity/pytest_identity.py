from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from mimesis import Address, Person
from mimesis.locales import Locale

from server.apps.identity.models import User


@pytest.fixture()
@pytest.mark.django_db()
def registered_user(client: Client) -> None:
    """Registered user fixture."""
    person = Person(Locale.EN)
    address = Address(Locale.EN)
    data = {
        'email': person.email(domains=['mimesis.name'], unique=True),
        'first_name': person.first_name(),
        'last_name': person.last_name(),
        'date_of_birth': '2023-03-05',
        'address': address.address(),
        'job_title': person.occupation(),
        'phone': person.telephone(),
        'password1': 'dd',
        'password2': 'dd',
    }
    response = client.post(reverse('identity:registration'), data=data)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('identity:login')

    user = User.objects.get(email=data['email'])
    user._password = data['password1']
    yield user


@pytest.fixture()
@pytest.mark.django_db()
def signedin_user(client: Client, registered_user: User) -> None:
    """Test successful login."""
    response = client.post(
        reverse('identity:login'),
        data={'username': registered_user.email, 'password': registered_user._password},
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('pictures:dashboard')

    return registered_user
