import os
from settings_common import *
import dj_database_url


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += (
    'storages',
)

# The host we send in email
HOST = 'signalback.com'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# this goes away when we switch to cleardb?
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_S3_SECURE_URLS = False       # use http instead of https
AWS_QUERYSTRING_AUTH = False     # don't add complex authentication-related query parameters for requests

# Write our logs to stderr for heroku
MIDDLEWARE_CLASSES += (
    'items.middleware.exception_logging_middleware.ExceptionLoggingMiddleware',
)

LOGGING = {
    'version': 1,
    'root': {'level': 'DEBUG' if DEBUG else 'INFO'},
}