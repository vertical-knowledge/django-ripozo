from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django_ripozo import DjangoDispatcher

import mock
import re
import unittest2


class TestDjangoDispatcher(unittest2.TestCase):
    def test_url_map(self):
        d = DjangoDispatcher()
        self.assertEqual(len(d.url_map), 1)
        self.assertIn('^$', d.url_map)

    def test_base_url(self):
        d = DjangoDispatcher(base_url='blah')
        self.assertEqual(d.base_url, 'blah')

    def test_url_patterns(self):
        """
        Test to ensure that the url_patterns propery
        appropriately gets the django patterns object
        """
        d = DjangoDispatcher()
        self.assertIsInstance(d.url_patterns, list)
        self.assertEqual(len(d.url_patterns), 1)

        def fake():
            pass
        d.register_route('fake', endpoint_func=fake, route='route', methods=['GET'])
        route = DjangoDispatcher._convert_url_to_regex('route')
        self.assertIsInstance(d.url_patterns, list)
        regexes = [p._regex for p in d.url_patterns]
        self.assertEqual(len(regexes), 2)
        self.assertIn(route, regexes)
        self.assertIn('^$', regexes)

    def test_register_route(self):
        d = DjangoDispatcher(method_route_class=mock.MagicMock())
        d.register_route('fake', route='fake2')
        mr = d.url_map['^fake2$']
        self.assertIsInstance(mr, mock.MagicMock)
        self.assertEqual(mr.add_route.call_count, 2)

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
