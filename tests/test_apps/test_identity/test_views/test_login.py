import json
from http import HTTPStatus
from typing import TYPE_CHECKING, Callable, Dict, Final

import httpretty
import pytest
from django.contrib import auth
from django.urls import reverse
from typing_extensions import Unpack

from server.apps.identity.models import User
from server.apps.identity.views.login import LoginView, RegistrationView

if TYPE_CHECKING:
    from plugins.identity.login import LoginData, LoginDataFactory
    from plugins.identity.registration import (
        RegistrationData,
        RegistrationDataFactory,
    )
    from plugins.identity.user import (
        ExternalAPIUserResponse,
        UserAssertion,
        UserData,
        UserExternalAssertion,
    )


EMPTY_FIELD: Final = ''


@pytest.mark.usefixtures('_unauthorized_client')
@pytest.mark.django_db()
class TestLogin(object):
    """A class for testing the logic of one-factor user authorization."""

    testdata = (
        {'username': EMPTY_FIELD},
        {'password': EMPTY_FIELD},
        {'username': EMPTY_FIELD, 'password': EMPTY_FIELD},
    )

    _url = reverse('identity:login')

    def test_login_page_renders(self) -> None:
        """Users can see the login page."""
        # Act
        response = self.client.get(self._url)
        resolver_func = response.resolver_match.func.__name__
        templates = [template.name for template in response.templates]

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert resolver_func == LoginView.as_view().__name__
        assert response.context['form']
        assert 'identity/pages/login.html' in templates

    @pytest.mark.usefixtures('_mock_check_pass')
    def test_login_of_registered_user(
        self,
        login_data: 'LoginData',
        get_user: User,
    ) -> None:
        """Login is successful for registered user."""
        # Act
        response = self.client.post(path=self._url, data=login_data)

        # Assert
        assert response.status_code == HTTPStatus.FOUND
        assert response.get('Location') == reverse('pictures:dashboard')
        assert get_user.check_password(login_data['password'])

    def test_login_of_unregistered_user(self, login_data: 'LoginData') -> None:
        """Login fails for unregistered user."""
        # Act
        response = self.client.post(path=self._url, data=login_data)
        user = auth.get_user(self.client)

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert not user.is_authenticated
        assert not User.objects.filter(email=login_data['username']).exists()

    @pytest.mark.parametrize(
        'required_fields',
        testdata,
        ids=[
            'empty_username_field',
            'empty_password_field',
            'empty_username_and_password_fields',
        ],
    )
    def test_login_with_empty_required_fields(
        self,
        required_fields: Dict[str, str],
        login_data_factory: 'LoginDataFactory',
    ) -> None:
        """Login fails if required fields (username, password) not provided."""
        # Arrange
        login_data = login_data_factory(**required_fields)

        # Act
        response = self.client.post(path=self._url, data=login_data)
        user = auth.get_user(self.client)

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert not user.is_authenticated

    @pytest.mark.usefixtures('_generate_credentials')
    def test_login_with_invalid_credentials(self) -> None:
        """Login fails if required fields (username, password) invalid."""
        # Arrange
        login_data = {'username': self.username, 'password': self.password}

        # Act
        response = self.client.post(path=self._url, data=login_data)
        user = auth.get_user(self.client)

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert not user.is_authenticated


@pytest.mark.usefixtures('_unauthorized_client')
@pytest.mark.django_db()
class TestRegistration(object):
    """A class for testing user authentication logic."""

    _url = reverse('identity:registration')

    def test_registration_page_renders(self) -> None:
        """Users can see the registration page."""
        # Act
        response = self.client.get(self._url)
        resolver_func = response.resolver_match.func.__name__
        templates = [template.name for template in response.templates]

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert resolver_func == RegistrationView.as_view().__name__
        assert response.context['form']
        assert 'identity/pages/registration.html' in templates

    def test_registration_with_valid_user(
        self,
        registration_data: 'RegistrationData',
        expected_user_data: 'UserData',
        assert_correct_user: 'UserAssertion',
    ) -> None:
        """Registration correct works with valid user data."""
        # Arrange
        passwords = (
            registration_data['password1'], registration_data['password2'],
        )

        # Act
        response = self.client.post(path=self._url, data=registration_data)
        user = User.objects.get(email=registration_data['email'])

        # Assert
        assert response.status_code == HTTPStatus.FOUND
        assert response.get('Location') == reverse('identity:login')
        assert_correct_user(registration_data['email'], expected_user_data)
        for pwd in passwords:
            assert user.check_password(pwd)

    @pytest.mark.parametrize(
        'field', User.REQUIRED_FIELDS + [User.USERNAME_FIELD],
    )
    def test_registration_without_required_field(
        self,
        registration_data_factory: 'RegistrationDataFactory',
        field: Unpack['RegistrationData'],
    ) -> None:
        """Test that missing required will fail the registration."""
        # Arrange
        post_data = registration_data_factory(
            **{field: EMPTY_FIELD},
        )

        # Act
        response = self.client.post(path=self._url, data=post_data)

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert not User.objects.filter(email=post_data['email']).exists()

    def test_registration_user_who_already_exists(
        self,
        registration_data: 'RegistrationData',
        get_user: User,
    ) -> None:
        """Registration fails if user has already registered."""
        # Arrange
        registration_data['email'] = get_user.email

        # Act
        response = self.client.post(path=self._url, data=registration_data)

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert User.objects.filter(email=registration_data['email']).exists()

    def test_registration_for_external_api_call(
        self,
        registration_data: 'RegistrationData',
        external_api_user_call_mock: 'ExternalAPIUserResponse',
        expected_user_data: 'UserData',
        assert_correct_external_user: 'UserExternalAssertion',
    ) -> None:
        """Registration works for external api call with correct user data."""
        # Act
        response = self.client.post(path=self._url, data=registration_data)

        # Assert
        assert response.status_code == HTTPStatus.FOUND
        assert response.get('Location') == reverse('identity:login')
        assert_correct_external_user(
            external_api_user_call_mock,
            expected_user_data,
        )

    @httpretty.activate
    def test_registration_for_external_api(  # noqa: WPS211
        self,
        registration_data: 'RegistrationData',
        expected_user_data: 'UserData',
        external_api_url_factory: Callable[[str], str],
        external_api_user_response: 'ExternalAPIUserResponse',
        assert_correct_external_user: 'UserExternalAssertion',
    ) -> None:
        """Registration works correctly if using external API.

        API url call is redirected to external JSON Server.
        """
        httpretty.register_uri(
            method=httpretty.POST,
            uri=external_api_url_factory('users'),
            body=json.dumps(external_api_user_response),
            content_type='application/json',
        )
        response = self.client.post(path=self._url, data=registration_data)

        assert response.status_code == HTTPStatus.FOUND
        assert httpretty.has_request()
        assert httpretty.last_request().method == 'POST'
        assert httpretty.last_request().path == '/users'
        assert_correct_external_user(
            external_api_user_response,
            expected_user_data,
        )
