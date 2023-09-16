from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_registration_view(
    client: Client,
    user_model_data,
    registration_data,
    assert_user
) -> None:
    response = client.post(
        '/identity/registration',
        data=registration_data
    )
    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('identity:login')
    assert_user(registration_data['email'], user_model_data)


@pytest.mark.django_db
def test_login(
    client: Client,
    user_model_data,
    assert_user,
    create_user
) -> None:
    user = create_user
    data = {
        'username': user.email,
        'password': user.password
    }
    response = client.post(
        '/identity/login',
        data=data
    )
    assert response.status_code == HTTPStatus.OK
    assert_user(data['username'], user_model_data)


@pytest.mark.django_db
def test_user_update(
    client: Client,
    create_user,
    user_model_data,
    assert_user
):
    user = create_user
    user_model_data['email'] = 'mail@mail.com'
    data = user_model_data
    response = client.put(
        '/identity/update',
        data=data
    )
    assert response.status_code == HTTPStatus.FOUND
    assert_user(user.email, user_model_data)
