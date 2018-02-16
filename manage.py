#!/usr/bin/env python
"""
Wrapper around ``django-admin.py``.
This requires the environment variable ``DJANGO_ENV`` defining the deployment environment.
It defines ``DJANGO_SETTINGS_MODULE`` based on the current deployment environment.
"""
import os
import sys

from django.core.exceptions import ImproperlyConfigured


if __name__ == "__main__":
    DJANGO_ENV = os.environ.get("DJANGO_ENV")
    if DJANGO_ENV is None:
        raise ImproperlyConfigured("The deployment environment 'DJANGO_ENV' is not defined in environment variables.")

    os.environ["DJANGO_SETTINGS_MODULE"] = "platyplus.settings.{}".format(DJANGO_ENV)

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)