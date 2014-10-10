from distutils.core import setup

setup(
    name='unconference',
    version='0.2',
    pacakges=['unconference'],
    license='copyright NOI',
    long_description='A set of resusable apps to support an unconference',
    install_requires=[
        'django>=1.6.5',
        'south>=0.8.4',
        'django-ajax-selects',
        'djangorestframework',
        'requests',
        'beautifulsoup4',
        'eventbrite',
        'sorl-thumbnail',
        'django-phonenumber-field'
    ],
)
