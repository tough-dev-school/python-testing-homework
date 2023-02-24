from typing import final

from django.contrib import admin

from server.apps.identity.models import User
from server.common.django.admin import TimeReadOnlyMixin


@final
@admin.register(User)
class UserAdmin(TimeReadOnlyMixin, admin.ModelAdmin[User]):
    """This class represents `User` in admin panel."""

    list_display = tuple(['id'] + User.REQUIRED_FIELDS)
    search_fields = (
        'email',
        'first_name',
        'last_name',
    )
