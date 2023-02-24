import punq
from django.conf import settings

from server.common.django.types import Settings

container = punq.Container()

# Custom dependencies go here:
# TODO: add custom deps

# Django stuff:
container.register(Settings, instance=settings)
