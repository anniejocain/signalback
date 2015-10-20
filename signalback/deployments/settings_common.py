import os, sys

# PROJECT_ROOT is the absolute path to the perma_web folder
# We determine this robustly thanks to http://stackoverflow.com/a/2632297
this_module = unicode(
    sys.executable if hasattr(sys, "frozen") else __file__,
    sys.getfilesystemencoding())
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(this_module)))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'items',
    'tastypie',
    'django_forms_bootstrap',
    'kombu.transport.django', # Using the Django DB as our broker. We should NOT do this in production
    'pipeline', # cache bust and compress our js and css
    
)

DATABASES = {}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.

USE_TZ = True

TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True


AUTH_USER_MODEL = 'items.SBUser'


STATIC_ROOT = '{0}/collected-static/'.format(PROJECT_ROOT)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
    'pipeline.finders.FileSystemFinder',
    'pipeline.finders.CachedFileFinder',
)

# Django Pipeline config
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_COMPILERS = (
    'pipeline_compass.compiler.CompassCompiler',
)

PIPELINE_JS = {}

PIPELINE_CSS = {
    'common': {
        'source_filenames': (
            'css/normalize.css',
            'css/skeleton.css',
            'css/style.scss',
        ),
        'output_filename': 'css/common-bundle.css',
    },

    'landing': {
        'source_filenames': (
        ),
        'output_filename': 'css/landing-bundle.css',
    },
    
    'items': {
        'source_filenames': (
        ),
        'output_filename': 'css/items-bundle.css',
    },
    
    
}

# We likely want to do something like this:
# PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.jsmin.JSMinCompressor'
PIPELINE_JS_COMPRESSOR = None
PIPELINE_CSS_COMPRESSOR = None

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',  
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# override to change .js mimetype from application/javascript for ie8 and below
# see http://django-pipeline.readthedocs.org/en/latest/configuration.html#pipeline-mimetypes
PIPELINE_MIMETYPES = (
  (b'text/coffeescript', '.coffee'),
  (b'text/less', '.less'),
  (b'text/javascript', '.js'),
  (b'text/x-sass', '.sass'),
  (b'text/x-scss', '.scss')
)

ROOT_URLCONF = 'signalback.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'

# Celery/Broker stuff
BROKER_URL = 'django://'

DEFAULT_FROM_EMAIL = 'SignalBack <info@signalback.com>'

TASTYPIE_DEFAULT_FORMATS = ['json', 'jsonp']