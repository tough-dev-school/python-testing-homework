from typing import TYPE_CHECKING

import pytest

from server.apps.identity.models import User

if TYPE_CHECKING:
    from plugins.identity.user import UserAssertion, UserData


@pytest.mark.django_db()
class TestUserModel(object):
    """A class for testing the User model."""

    def test_create_user(
        self,
        create_user: User,
        expected_user_data: 'UserData',
        assert_correct_user: 'UserAssertion',
    ) -> None:
        """Correct user creation in the database."""
        # Assert
        assert_correct_user(create_user.email, expected_user_data)

    @pytest.mark.usefixtures('_generate_credentials')
    def test_create_user_through_manager(
        self,
        user_data: 'UserData',
        expected_user_data: 'UserData',
        assert_correct_user: 'UserAssertion',
    ) -> None:
        """Correct creation of a user in the database via the user manager."""
        # Act
        user = User.objects.create_user(**user_data, password=self.password)

        # Assert
        assert_correct_user(user.email, expected_user_data)
        assert user.check_password(self.password)
        assert not user.is_superuser
        assert not user.is_staff

    @pytest.mark.usefixtures('_generate_credentials')
    def test_fails_create_user(
        self,
        user_data: 'UserData',
        assert_correct_user: 'UserAssertion',
    ) -> None:
        """Fail creation of a user without email."""
        # Arrange
        user_data['email'] = ''

        # Act
        with pytest.raises(ValueError, match='email') as exc_info:
            User.objects.create_user(**user_data, password=self.password)

        # Assert
        assert 'Users must have an email' in str(exc_info.value)  # noqa: WPS441
        assert not User.objects.filter(email=user_data['email']).exists()

    @pytest.mark.usefixtures('_generate_credentials')
    def test_create_superuser(
        self,
        user_data: 'UserData',
        expected_user_data: 'UserData',
        assert_correct_user: 'UserAssertion',
    ) -> None:
        """Correct creation of a superuser in the database."""
        # Act
        user = User.objects.create_superuser(
            **user_data, password=self.password,
        )

        # Assert
        assert user.email == expected_user_data['email']
        assert user.check_password(self.password)
        assert user.is_superuser
        assert user.is_staff

    def test_update_user(
        self,
        get_user: User,
        expected_user_data: 'UserData',
    ) -> None:
        """Correct updating of user data in the database."""
        # Arrange
        user = get_user
        user.job_title = 'CEO'
        user.save()

        # Act
        user_from_db = User.objects.get(job_title='CEO')

        # Assert
        assert user.id == user_from_db.id
        assert user.job_title != expected_user_data['job_title']

    def test_delete_user(self, get_user: User) -> None:
        """Correct deletion of the user from the database."""
        # Arrange
        user_from_db = User.objects.get(pk=get_user.id)

        # Act
        User.objects.filter(pk=user_from_db.id).delete()

        # Assert
        assert not User.objects.filter(pk=user_from_db.id).exists()
