from .base import *

DEBUG = False

# CORS_ORIGIN_ALLOW_ALL = True  # TODO refine to heroku domain only
CORS_ORIGIN_REGEX_WHITELIST = (r'^(https?://)?(\w+\.)?heroku\.com$', )
