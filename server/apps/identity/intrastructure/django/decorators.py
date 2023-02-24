from typing import Any, Callable, TypeVar

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

_CallableT = TypeVar('_CallableT', bound=Callable[..., Any])


def redirect_logged_in_users(
    *,
    redirect_field_name: str = '',
) -> Callable[[_CallableT], _CallableT]:
    """Decorator for views that checks that the user is NOT logged in."""
    return user_passes_test(
        lambda user: not user.is_authenticated,
        login_url=settings.LOGIN_REDIRECT_URL,
        redirect_field_name=redirect_field_name,
    )
