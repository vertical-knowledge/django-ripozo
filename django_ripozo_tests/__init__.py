from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

__author__ = 'Tim Martin'


base_dir = os.path.dirname(__file__)
project = os.path.join(base_dir, '..', 'test_app')
# os.environ['PATH'] += ':{0}'.format(project)
# os.environ['PATH'] += ':{0}'.format(os.path.join(project, 'test_project'))
# os.environ['PATH'] += ':{0}'.format(os.path.join(project, 'testapp'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'

from . import helpers, integration, unit
