from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

SECRET_KEY = 'not a secret'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

INSTALLED_APPS = (
    'manager',
)