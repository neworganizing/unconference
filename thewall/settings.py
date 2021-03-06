"""Unconference Project Settings"""

import dj_database_url
from os import environ

from unipath import FSPath as Path

# Helper lambda for gracefully degrading env variables. Taken from http://rdegges.com/devops-django-part-3-the-heroku-way
env = lambda e, d: environ[e] if environ.has_key(e) else d

# EventBrite API Info
EB_APPKEY = env('EB_APPKEY', None)
EB_USERKEY = env('EB_USERKEY', None)
EB_OAUTHKEY = env('EB_OAUTHKEY', None)
EB_EVENTID = env('EB_EVENTID', None)

# Google Aanalytics Information
GA_ID = env('GA_ID', None)
GA_DOMAIN = env('SITE_DOMAIN', None)

BASE = Path(__file__).absolute().ancestor(2)
APP = Path(__file__).absolute().ancestor(1)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


MEDIA_URL = '/media/'

if environ.has_key('AWS_STORAGE_BUCKET'):
    AWS_STORAGE_BUCKET_NAME = environ['AWS_STORAGE_BUCKET']
    AWS_ACCESS_KEY_ID = environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = environ['AWS_SECRET_ACCESS_KEY']
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
    STATIC_URL = S3_URL
    ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
else:
    STATIC_URL = '/static/'


MEDIA_ROOT = BASE.child('media')
STATIC_ROOT = BASE.child('static')
STATICFILES_DIRS = (
    BASE.child('design'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = env('SECRET_KEY', 'lo7i8ko)i00be5!%45*l2i6_1$5ylbkv-w1nk87#ge9f^)(cv@')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'thewall.session.processors.general',
    'thewall.session.processors.session_times',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'thewall.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'thewall.wsgi.application'

TEMPLATE_DIRS = [APP.child('templates')]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

	# Django Admin Related Apps
    'django.contrib.admin',
    'django.contrib.admindocs',

	# Heroku Specific Apps Here
	'gunicorn',

	# 3rd Party Apps We Need
	'djangorestframework',
    'storages',
    'boto',
	'ajax_select',

	# Our Apps
	'thewall'
)

# Third party configuration

# define the lookup channels in use on the site
AJAX_LOOKUP_CHANNELS = {
    #   pass a dict with the model and the field to search against
    'participant'  : {'model':'participants.participant', 'search_field':'name'}
}

# magically include jqueryUI/js/css
AJAX_SELECT_BOOTSTRAP = True
AJAX_SELECT_INLINES = 'inline'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Import from localsettings
try:
    from thewall.localsettings import *
except ImportError:
    pass
