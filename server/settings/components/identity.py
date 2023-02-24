from django.urls import reverse_lazy

# Django authentication system
# https://docs.djangoproject.com/en/3.2/topics/auth/

AUTH_USER_MODEL = 'identity.User'

AUTHENTICATION_BACKENDS = (
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
)

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]


# Login settings
# https://docs.djangoproject.com/en/3.2/ref/settings/

LOGIN_URL = reverse_lazy('identity:login')
LOGIN_REDIRECT_URL = reverse_lazy('pictures:dashboard')
LOGOUT_REDIRECT_URL = reverse_lazy('index')


# django-ratelimit
# https://django-ratelimit.readthedocs.io/en/stable/

RATELIMIT_ENABLE = True


# django-axes
# https://django-axes.readthedocs.io/

AXES_ONLY_USER_FAILURES = True
AXES_RESET_ON_SUCCESS = True
AXES_FAILURE_LIMIT = 5


# django-password-reset
# https://django-password-reset.readthedocs.io

PASSWORD_RESET_TOKEN_EXPIRES = 3600  # one hour
RECOVER_ONLY_ACTIVE_USERS = True
