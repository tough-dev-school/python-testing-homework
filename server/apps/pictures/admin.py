from typing import final

from django.contrib import admin

from server.apps.pictures.models import FavouritePicture
from server.common.django.admin import TimeReadOnlyMixin


@final
@admin.register(FavouritePicture)
class FavouritePictureAdmin(
    TimeReadOnlyMixin,
    admin.ModelAdmin[FavouritePicture],
):
    """This class represents `FavouritePicture` in admin panel."""

    list_display = ('id', 'foreign_id', 'url', 'user_id')
    list_select_related = ('user',)
    raw_id_fields = ('user',)
