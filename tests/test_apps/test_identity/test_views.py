from http import HTTPStatus
from typing import Type

import pytest
from django.db import models
from django.test import Client
from django.urls import reverse


@pytest.fixture()
def user(django_user_model: models.Model):
    return django_user_model.objects.create_user(email='user1@example.com', password='password1')


@pytest.fixture()
def user_client(client: Client, user) -> Client:
    client.force_login(user)
    return client

@pytest.mark.django_db()
def test_anonymous_can_open_login_page(client: Client):
    response = client.get(reverse('identity:login'))

    assert response.status_code == HTTPStatus.OK
    assert response.get('Content-Type').startswith('text/html')


def test_user_is_redirected_to_dashboard_from_login_page(user_client: Client):
    response = user_client.get(reverse('identity:login'))

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('pictures:dashboard')


def test_user_is_redirected_to_main_page_on_logout(user_client: Client):
    response = user_client.post(reverse('identity:logout'))

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('index')


def test_anonymous_is_redirected_to_login_from_update_user_page(client: Client):
    response = client.get(reverse('identity:user_update'))

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location').startswith(reverse('identity:login'))


def test_anonymous_cannot_sent_update_user_request(client: Client):
    response = client.post(reverse('identity:user_update'), data={})

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location').startswith(reverse('identity:login'))


def test_user_can_open_user_update_page(user_client: Client):
    response = user_client.get(reverse('identity:user_update'))

    assert response.status_code == HTTPStatus.OK


def test_user_can_update_their_info(user_client: Client, user, django_user_model: models.Model):
    user_data = {
        'first_name': 'new first name',
        'last_name': 'new last name',
        'date_of_birth': '01.01.1970',
        'address': 'new address',
        'job_title': 'new job title',
        'phone': 'new phone number',
    }

    response = user_client.post(reverse('identity:user_update'), data=user_data)

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('identity:user_update')
    user.refresh_from_db()
    assert user.first_name == user_data['first_name']
    assert user.last_name == user_data['last_name']


def test_user_registration(client: Client, django_user_model):
    new_user_data = {
        'email': 'user1@example.com',
        'first_name': 'first name',
        'last_name': 'last name',
        'date_of_birth': '01.01.1990',
        'address': 'some address',
        'job_title': 'some job title',
        'phone': 'some phone number',
    }

    response = client.post(reverse('identity:registration'), data=new_user_data)

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == ''
    user = django_user_model.objects.get(email='user1@example.com')
    assert user.first_name == new_user_data['first_name']
    assert user.last_name == new_user_data['last_name']
