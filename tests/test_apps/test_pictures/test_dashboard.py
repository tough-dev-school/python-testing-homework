from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture
from server.apps.pictures.views import DashboardView

if TYPE_CHECKING:
    from plugins.pictures.picture import PictureData


@pytest.mark.django_db()
def test_view_dashboard_renders(
    client: Client,
    get_user: User,
    picture_data: 'PictureData',
) -> None:
    """Test correct picture adding."""
    # Arrange
    client.force_login(get_user)

    # Act
    response = client.post(reverse('pictures:dashboard'), data=picture_data)
    resolver_func = response.resolver_match.func.__name__

    # Assert
    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('pictures:dashboard')
    assert resolver_func == DashboardView.as_view().__name__
    assert FavouritePicture.objects.get(user=get_user)
