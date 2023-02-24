from typing import final

import attr

from server.apps.identity.intrastructure.services import placeholder
from server.apps.identity.models import User
from server.common.django.types import Settings


@final
@attr.dataclass(slots=True, frozen=True)
class UserCreateNew(object):
    """
    Create new user in :term:`Placeholder API`.

    Get their :term:`lead_id` back and save it locally.

    .. warning:
        This use-case does not handle transactions!

    """

    _settings: Settings

    def __call__(self, user: User) -> None:
        """
        Execute the usecase.

        Ideally this docstring must contain a link to the user-story, like:
        https://sobolevn.me/2019/02/engineering-guide-to-user-stories
        """
        new_ids = self._create_lead(user)
        return self._update_user_ids(user, new_ids)

    def _create_lead(self, user: User) -> placeholder.UserResponse:
        return placeholder.LeadCreate(
            api_url=self._settings.PLACEHOLDER_API_URL,
            api_timeout=self._settings.PLACEHOLDER_API_TIMEOUT,
        )(user=user)

    def _update_user_ids(
        self,
        user: User,
        new_ids: placeholder.UserResponse,
    ) -> None:
        # This can be moved to some other place once this becomes too complex:
        user.lead_id = new_ids.id
        user.save(update_fields=['lead_id'])
