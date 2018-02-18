from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CORS_ORIGIN_ALLOW_ALL = True  # TODO refine to heroku domain only
