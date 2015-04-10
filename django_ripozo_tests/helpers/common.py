from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.core.management import call_command

from django.test import TestCase

from ripozo_tests.python2base import TestBase

import django
import os


class UnittestBase(TestBase):
    @classmethod
    def setUpClass(cls):
        try:
            django.setup()
        except AttributeError:
            pass
        call_command('syncdb', interactive=False)
        try:
            call_command('makemigrations', interactive=False)
            call_command('migrate', interactive=False)
        except:
            pass