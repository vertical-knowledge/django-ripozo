from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.core.management import call_command

import cProfile
import django
import random
import pstats
import string


def profileit(func):
    """
    Decorator straight up stolen from stackoverflow
    """
    def wrapper(*args, **kwargs):
        datafn = func.__name__ + ".profile" # Name the data file sensibly
        prof = cProfile.Profile()
        prof.enable()
        retval = prof.runcall(func, *args, **kwargs)
        prof.disable()
        stats = pstats.Stats(prof)
        try:
            stats.sort_stats('cumtime').print_stats(10)
        except KeyError:
            pass  # breaks in python 2.6
        try:
            stats.sort_stats('tottime').print_stats(10)
        except KeyError:
            pass  # breaks in python 2.6
        return retval

    return wrapper


def random_string(length=50):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


class UnittestBase(object):
    @classmethod
    def setUpClass(cls):
        try:
            django.setup()
        except AttributeError:
            pass
        call_command('syncdb', interactive=False)
        try:
            call_command('makemigrations')
            call_command('migrate', interactive=False)
        except:
            pass
