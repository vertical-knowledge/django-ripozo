from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ripozo_tests.python2base import TestBase

import django
import os


class UnittestBase(TestBase):
    def setUp(self):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'django_ripozo_tests.helpers.django_settings'
        django.setup()