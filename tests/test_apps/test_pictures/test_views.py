import pytest
from django.test import Client, RequestFactory
from django.urls import reverse

from server.apps.identity.models import User
from server.apps.pictures.views import DashboardView

pytestmark = [pytest.mark.django_db]


def test_pictures_in_context_data(authorized_client: Client):
    url = reverse('pictures:dashboard')
    response = authorized_client.post(url)
    assert "pictures" in response.context


def test_user_in_form_kwargs(user: User, request_factory: RequestFactory):
    url = reverse('pictures:dashboard')
    request = request_factory.post(url)
    request.user = user

    view = DashboardView()
    view.setup(request)
    form_kwargs = view.get_form_kwargs()

    assert "user" in form_kwargs
