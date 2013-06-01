from .base import *

ROOT_URLCONF = 'bawebauth.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'south',

    'bawebauth.libs.yamlcss',
    'bawebauth.libs.jdatetime',

    'bawebauth.apps.bawebauth',

    'django.contrib.admin',
    'django.contrib.admindocs',

    'compressor',
)

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/?next=%s' % LOGOUT_REDIRECT_URL
