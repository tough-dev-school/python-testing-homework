import pytest

from server.apps.identity.models import User


@pytest.mark.django_db()
def test_create_user(
    create_user: User,
    user_data,
    assert_correct_user,
) -> None:
    """Correct user creation in the database."""
    # Assert
    assert_correct_user(create_user.email, user_data)


def test_update_user(
    create_user: User,
    user_data,
) -> None:
    """Correct updating of user data in the database."""
    # Arrange
    create_user.job_title = 'CEO'
    create_user.save()

    # Act
    user_from_db = User.objects.get(job_title='CEO')

    # Assert
    assert create_user.id == user_from_db.id
    assert create_user.job_title != user_data['job_title']


def test_delete_user(create_user: User) -> None:
    """Correct deletion of the user from the database."""
    # Arrange
    user_from_db = User.objects.get(pk=create_user.id)

    # Act
    User.objects.filter(pk=user_from_db.id).delete()

    # Assert
    assert not User.objects.filter(pk=user_from_db.id).exists()
