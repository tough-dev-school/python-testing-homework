from http import HTTPStatus
from typing import TYPE_CHECKING, Final

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User
from server.apps.identity.views.login import LoginView, RegistrationView

if TYPE_CHECKING:
    from plugins.identity.login import LoginData, LoginDataFactory
    from plugins.identity.registration import (
        RegistrationData,
        RegistrationDataFactory,
    )
    from plugins.identity.user import UserAssertion, UserData


EMPTY_FIELD: Final = ''


@pytest.mark.django_db()
class TestLogin(object):
    """A class for testing the logic of one-factor user authorization."""

    URl = '/identity/login'

    def test_login_page_renders(self, client: Client) -> None:
        """Users can see the login page."""
        # Act
        response = client.get(self.URl)
        resolver_func = response.resolver_match.func.__name__
        templates = [template.name for template in response.templates]

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert resolver_func == LoginView.as_view().__name__
        assert response.context['form']
        assert 'identity/pages/login.html' in templates

    @pytest.mark.usefixtures('mock_check_pass')
    def test_success_login_of_registered_user(
        self,
        client: Client,
        login_data: 'LoginData',
        get_user: User,
    ) -> None:
        """Login is successful for registered user."""
        # Act
        response = client.post(self.URl, data=login_data)

        # Assert
        assert response.status_code == HTTPStatus.FOUND
        assert response.get('Location') == reverse('pictures:dashboard')

    def test_fails_login_of_unregistered_user(
        self,
        client: Client,
        login_data: 'LoginData',
    ) -> None:
        """Login fails for registered user."""
        # Act
        response = client.post(self.URl, data=login_data)

        # Assert
        assert response.status_code == HTTPStatus.OK

    def test_fails_login_without_username(
        self,
        client: Client,
        login_data_factory: 'LoginDataFactory',
    ) -> None:
        """Login fails if not username provided."""
        # Arrange
        login_data = login_data_factory(username=EMPTY_FIELD)

        # Act
        response = client.post(self.URl, data=login_data)

        # Assert
        assert response.status_code == HTTPStatus.OK

    def test_fails_login_without_password(
        self,
        client: Client,
        login_data_factory: 'LoginDataFactory',
    ) -> None:
        """Login fails if not password provided."""
        # Arrange
        login_data = login_data_factory(password=EMPTY_FIELD)

        # Act
        response = client.post(self.URl, data=login_data)

        # Assert
        assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
class TestRegistration(object):
    """A class for testing user authentication logic."""

    URL = '/identity/registration'

    def test_registration_page_renders(
        self,
        client: Client,
        user_data: 'UserData',
    ) -> None:
        """Users can see the registration page."""
        # Act
        response = client.get(self.URL)
        resolver_func = response.resolver_match.func.__name__
        templates = [template.name for template in response.templates]

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert resolver_func == RegistrationView.as_view().__name__
        assert response.context['form']
        assert 'identity/pages/registration.html' in templates

    def test_success_registration_with_valid_user(
        self,
        client: Client,
        user_data: 'UserData',
        registration_data: 'RegistrationData',
        assert_correct_user: 'UserAssertion',
    ) -> None:
        """Registration correct works with valid user data."""
        # Act
        response = client.post(self.URL, data=registration_data)
        user = User.objects.filter(email=registration_data['email'])

        # Assert
        assert response.status_code == HTTPStatus.FOUND
        assert response.get('Location') == reverse('identity:login')
        assert_correct_user(registration_data['email'], user_data)
        assert user.exists()

    @pytest.mark.parametrize(
        'field', User.REQUIRED_FIELDS + [User.USERNAME_FIELD]
    )
    def test_fails_registration_with_missing_required_field(
        self,
        client: Client,
        registration_data_factory: 'RegistrationDataFactory',
        field: str,
    ) -> None:
        """Test that missing required will fail the registration."""
        # Arrange
        post_data = registration_data_factory(
            **{field: EMPTY_FIELD},  # type: ignore[arg-type]
        )

        # Act
        response = client.post(self.URL, data=post_data)
        user = User.objects.filter(email=post_data['email'])

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert not user.exists()

    def test_fails_registration_user_which_has_already_registered(
        self,
        client: Client,
        registration_data: 'RegistrationData',
        get_user: User,
    ) -> None:
        """Registration fails if user has already registered."""
        # Arrange
        registration_data['email'] = get_user.email

        # Act
        response = client.post(self.URL, data=registration_data)

        # Assert
        assert response.status_code == HTTPStatus.OK
