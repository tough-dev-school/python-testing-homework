import punq
from django.conf import settings

# UseCases
from server.apps.identity.logic.usecases.user_create_new import UserCreateNew
from server.apps.identity.logic.usecases.user_update import UserUpdate
from server.common.django.types import Settings

container = punq.Container()

# Custom dependencies go here:
# TODO: add custom deps

# Django stuff:
container.register(Settings, instance=settings)
instance_settings = container.resolve(Settings)

user_create_new = UserCreateNew(settings=instance_settings)
container.register(UserCreateNew, instance=user_create_new)

user_update = UserUpdate(settings=instance_settings)
container.register(UserUpdate, instance=user_update)
