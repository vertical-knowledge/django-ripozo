from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.test import Client

from django_ripozo_tests.helpers.common import UnittestBase

import json
import logging
import six
import unittest

logger = logging.getLogger(__name__)


class TestBasic(UnittestBase, unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_list_url(self):
        response = self.client.get('/api/myresource/')
        self.assertEqual(response.status_code, 200)
        content = six.text_type(response.content, 'utf8')
        data = json.loads(content)
        self.assertDictEqual(data['properties'], dict(hello='world'))

    def test_individual_url(self):
        response = self.client.get('/api/myidresource/1/')
        self.assertEqual(response.status_code, 200)
        content = six.text_type(response.content, 'utf8')
        data = json.loads(content)
        self.assertDictEqual(data['properties'], dict(hello='world', id='1'))
