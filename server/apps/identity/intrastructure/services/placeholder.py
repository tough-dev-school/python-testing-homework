from typing import Dict, final

import requests

from server.apps.identity.models import User
from server.common import pydantic_model
from server.common.services import http


@final
class UserResponse(pydantic_model.BaseModel):
    """Schema for API response with :term:`lead_id`."""

    id: int


# TODO: use redis-based caching
@final
class LeadCreate(http.BaseFetcher):
    """Service around creating new users and fething their :term:`lead_id`."""

    _url_path = '/users'

    def __call__(
        self,
        *,
        user: User,
    ) -> UserResponse:
        """Create remote user and return assigned ids."""
        response = requests.post(
            self.url_path(),
            json=_serialize_user(user),
            timeout=self._api_timeout,
        )
        response.raise_for_status()
        return UserResponse(**response.json())


@final
class LeadUpdate(http.BaseFetcher):
    """Service around editing users."""

    _url_path = '/users/{0}'

    def __call__(
        self,
        *,
        user: User,
    ) -> None:
        """Update remote user."""
        response = requests.patch(
            self.url_path().format(user.lead_id),
            json=_serialize_user(user),
            timeout=self._api_timeout,
        )
        response.raise_for_status()


def _serialize_user(user: User) -> Dict[str, str]:
    return {
        'name': user.first_name,
        'last_name': user.last_name,
        'birthday': user.date_of_birth.strftime('%d.%m.%Y'),
        'city_of_birth': user.address,
        'position': user.job_title,
        'email': user.email,
        'phone': user.phone,
    }
