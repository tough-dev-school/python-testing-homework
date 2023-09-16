import pytest
from django.test import Client
from django.urls import reverse
from http import HTTPStatus
from django.contrib.auth import get_user_model



@pytest.mark.django_db()
def test_get_pictures_dashboard(admin_client: Client):
    url = reverse('pictures:dashboard')
    response =admin_client.get(url)
    assert response.status_code == HTTPStatus.OK
