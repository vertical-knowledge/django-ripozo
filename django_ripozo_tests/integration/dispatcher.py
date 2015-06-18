from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django_ripozo.dispatcher import DjangoDispatcher, MethodRouter

from django_ripozo_tests.helpers.common import UnittestBase

import unittest2


class TestDispatcher(UnittestBase, unittest2.TestCase):
    def test_register_route(self):
        """
        Tests the register_route method on the DjangoDispatcher instance
        """
        d = DjangoDispatcher()
        def fake():
            pass
        d.register_route('fake', endpoint_func=fake, route='route', methods=['GET'])
        route = DjangoDispatcher._convert_url_to_regex('route')
        self.assertIn(route, d.url_map)
        old_router = d.url_map[route]
        self.assertIsInstance(d.url_map[route], MethodRouter)
        def fake2():
            pass
        d.register_route('fake2', endpoint_func=fake2, route='route', methods=['POST'])
        self.assertEqual(old_router, d.url_map[route])
        self.assertEqual(len(old_router.method_map), 2)

    def test_url_patterns_property(self):
        """
        Test to ensure that the url_patterns propery
        appropriately gets the django patterns object
        """
        d = DjangoDispatcher()
        self.assertIsInstance(d.url_patterns, list)
        self.assertEqual(d.url_patterns, [])

        def fake():
            pass
        d.register_route('fake', endpoint_func=fake, route='route', methods=['GET'])
        route = DjangoDispatcher._convert_url_to_regex('route')
        self.assertIsInstance(d.url_patterns, list)
        self.assertEqual(d.url_patterns[0]._regex, route)
