"""
Django settings for platyplus project.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import environ
from django.utils.translation import gettext_lazy as _

WSGI_APPLICATION = 'platyplus.wsgi.application'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# =============================================================================
# Environment variables
# =============================================================================

# app:django-environ
env = environ.Env()

# Define the deployment environment we're running on.
# Note: No default value to never be "silently wrong".
DJANGO_ENV = env("DJANGO_ENV")

# Load environment variables from ``.env`` and ``.env_secrets``.
# Only in non-dockerized ``local`` deployment environment.
if DJANGO_ENV == "local" and env("DOCKERIZED", default=0) != 1:
    for file_path in (os.path.join(BASE_DIR, ".env"), os.path.join(BASE_DIR, ".env_secrets")):
        if os.path.exists(file_path):
            env.read_env(file_path)

# =============================================================================
# Project constants
# =============================================================================
# TODO

# =============================================================================
# Apps
# =============================================================================
# Best Practice: Specify the dotted path to the app config class, avoid using ``default_app_config``.
PROJECT_APPS = [
    'core',
    'users',
    'org_units',
    'links',
    'modules',
]
THIRD_PARTY_APPS = [
    'graphene_django',
    'corsheaders',
]
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
INSTALLED_APPS = PROJECT_APPS + THIRD_PARTY_APPS + DJANGO_APPS

# =============================================================================
# Middlewares
# =============================================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'graphql_jwt.middleware.JSONWebTokenMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =============================================================================
# Internationalization & localization
# =============================================================================
# https://docs.djangoproject.com/en/2.0/topics/i18n/
USE_I18N = True
USE_L10N = True
USE_TZ = True
# Default time zone, for the system and users.
DEFAULT_SYSTEM_TIME_ZONE = "UTC"
DEFAULT_USER_TIME_ZONE = "Europe/Brussels"
# Default time zone that Django will use to display datetimes in templates and to interpret datetimes entered in forms.
# Choices can be found here: https://en.wikipedia.org/wiki/List_of_tz_zones_by_name although not all choices
# may be available on all operating systems. In a Windows environment this must be set to your system time zone.
TIME_ZONE = DEFAULT_USER_TIME_ZONE
# Specify which languages are available for language selection.
# See: https://docs.djangoproject.com/en/1.11/ref/settings/#language-code
LANGUAGES = (
    ("en", _("English")),
    # ("fr", _("French")),
    # ("nl", _("Dutch")),
)
# Default language code, for the system and users.
DEFAULT_SYSTEM_LANGUAGE_CODE = "en"
DEFAULT_USER_LANGUAGE_CODE = "en"
# Language code for this installation.
LANGUAGE_CODE = DEFAULT_USER_LANGUAGE_CODE


# =============================================================================
# Filesystem paths
# =============================================================================


# =============================================================================
# URLs
# =============================================================================
ROOT_URLCONF = 'platyplus.urls'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = '/static/'
# Host/domain names that this Django site can serve.
# Default: Allow this domain and subdomains.
# ALLOWED_HOSTS = env.tuple("ALLOWED_HOSTS", default=(".{}".format(SITE_DOMAIN),))
# TODO too generic!!!
ALLOWED_HOSTS = ['*']


# =============================================================================
# Email
# =============================================================================


# =============================================================================
# Templates
# =============================================================================
# A list containing the settings for all template engines to be used with Django.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# =============================================================================
# Database
# =============================================================================
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
# Parse database configuration from $DATABASE_URL
try:
    import dj_database_url
    DATABASES = { 'default': dj_database_url.config(conn_max_age=500) }
    DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
except:
    pass


# =============================================================================
# Session
# =============================================================================


# =============================================================================
# Users & auth
# =============================================================================
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]
# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# =============================================================================
# Debugging
# =============================================================================
DEBUG = True  # TODO not in prod!!!


# =============================================================================
# Error & logging
# =============================================================================
# TODO


# =============================================================================
# Miscellaneous project settings
# =============================================================================
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")


# =============================================================================
# Third party app settings
# =============================================================================
GRAPHENE = {
    'SCHEMA': 'platyplus.schema.schema',
    'SCHEMA_OUTPUT': 'schema.json',
    # Max items returned in ConnectionFields / FilterConnectionFields
    'RELAY_CONNECTION_MAX_LIMIT': 100,
    'MIDDLEWARE': [
        'graphene_django.debug.DjangoDebugMiddleware',
    ]
}

GDAL_LIBRARY_PATH = os.getenv('GDAL_LIBRARY_PATH')
GEOS_LIBRARY_PATH = os.getenv('GEOS_LIBRARY_PATH')

