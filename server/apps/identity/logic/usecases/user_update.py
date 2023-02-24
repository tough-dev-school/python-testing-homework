from typing import final

import attr

from server.apps.identity.intrastructure.services import placeholder
from server.apps.identity.models import User
from server.common.django.types import Settings


@final
@attr.dataclass(slots=True, frozen=True)
class UserUpdate(object):
    """
    Update existing user in :term:`Placeholder API`.

    Get their :term:`lead_id` back and save it locally.

    .. warning:
        This use-case does not handle transactions!

    """

    _settings: Settings

    def __call__(self, user: User) -> None:
        """Update existing user in the remote api."""
        return self._update_lead(user)

    def _update_lead(self, user: User) -> None:
        return placeholder.LeadUpdate(
            api_url=self._settings.PLACEHOLDER_API_URL,
            api_timeout=self._settings.PLACEHOLDER_API_TIMEOUT,
        )(user=user)
