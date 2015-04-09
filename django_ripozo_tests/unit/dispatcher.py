from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django_ripozo.dispatcher import DjangoDispatcher

from django_ripozo_tests.helpers.common import UnittestBase

import unittest


class TestDispatcher(UnittestBase, unittest.TestCase):
    def test_base_url(self):
        """
        Tests the base_url property
        """
        d = DjangoDispatcher()
        self.assertEqual(d.base_url, '')
        d = DjangoDispatcher(base_url='base')
        self.assertEqual(d.base_url, 'base')

    def test_routers_property(self):
        """
        Tests the routers property
        """
        self.assertIsNone(DjangoDispatcher._routers)
        d = DjangoDispatcher()
        self.assertEqual(d.routers, {})
        d.routers['key'] = 'value'
        self.assertDictEqual(d.routers, {'key': 'value'})
        self.assertIsNone(DjangoDispatcher._routers)

    def test_url_map_property(self):
        """
        Tests the url_map property
        """
        self.assertIsNone(DjangoDispatcher._url_map)
        d = DjangoDispatcher()
        self.assertEqual(d.url_map, {})
        d.url_map['key'] = 'value'
        self.assertDictEqual(d.url_map, {'key': 'value'})
        self.assertIsNone(DjangoDispatcher._url_map)

    def test_convert_url_to_regex(self):
        """
        Tests the ``DjangoDispatcher_convert_url_to_regex`` static method
        """
        urls = [('/api/resource', '^api/resource$'),
                ('', '^$'),
                ('/api/resource/<id>', '^api/resource/(?P<id>[^/]+)$'),
                ('/api/resource/<id>/<pk>', '^api/resource/(?P<id>[^/]+)/(?P<pk>[^/]+)$'),
                ('/api/resource/<id>/<id>', '^api/resource/(?P<id>[^/]+)/(?P<id>[^/]+)$'),
                ('/api/resource/<id>/another', '^api/resource/(?P<id>[^/]+)/another$')]
        for input_url, output in urls:
            self.assertEqual(DjangoDispatcher._convert_url_to_regex(input_url), output)

    def test_register_route(self):
        """
        Tests the register_route method on the DjangoDispatcher instance
        """
        pass

    def test_url_patterns_property(self):
        """
        Test to ensure that the url_patterns propery
        appropriately gets the django patterns object
        """
        pass
