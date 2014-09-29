import sys
from django.conf import settings

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    ROOT_URLCONF='test_urls',
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'standalone_models',
        'thewall',
        'awards'
    ),
    USER_PROFILE_MODEL='standalone_models.UserProfile',
    ORGANIZATION_MODEL='standalone_models.Organization'
)

from django.test.simple import DjangoTestSuiteRunner
test_runner = DjangoTestSuiteRunner(verbosity=1)
failures = test_runner.run_tests(['thewall', 'awards'])
if failures:
    sys.exit(failures)
