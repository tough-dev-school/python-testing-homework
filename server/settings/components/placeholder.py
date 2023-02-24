# Custom settings for Placeholder API integration.
# All settings must be documented!

from server.settings.components import config

# API url we use to fetch data, can be switched from real Placeholder API
# to your custom one, that can be defined in `docker/placeholder`:
PLACEHOLDER_API_URL = config('DJANGO_PLACEHOLDER_API_URL')

# API default timeout in seconds:
PLACEHOLDER_API_TIMEOUT = config('DJANGO_PLACEHOLDER_API_TIMEOUT', cast=int)
