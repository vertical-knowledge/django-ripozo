from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.http import HttpResponseNotAllowed, HttpResponse

from django_ripozo.dispatcher import MethodRouter
from django_ripozo.exceptions import MethodNotAllowed

from django_ripozo_tests.helpers.common import UnittestBase

import mock
import unittest


class TestDispatcher(UnittestBase, unittest.TestCase):
    """
    unit tests for the ``MethodRouter`` class
    """

    def test_add_route(self):
        """
        Ensure that the add_route method works as intended
        """
        mr = MethodRouter(None, None)
        self.assertEqual(mr.method_map, {})
        def fake():
            pass
        mr.add_route(endpoint_func=fake, methods=['GET'])
        self.assertEqual(mr.method_map['get'], fake)
        self.assertRaises(ValueError, mr.add_route, endpoint_func=fake, methods=['GET'])
        self.assertRaises(ValueError, mr.add_route, endpoint_func=fake, methods=['get'])

        mr = MethodRouter(None, None)
        self.assertRaises(ValueError, mr.add_route, endpoint_func=fake, methods=['GET', 'get'])

        mr = MethodRouter(None, None)
        mr.add_route(endpoint_func=fake, methods=['POST', 'GET'])
        self.assertEqual(mr.method_map['get'], fake)
        self.assertEqual(mr.method_map['post'], fake)

        mr.add_route(endpoint_func=fake, methods=['PATCH', 'put'])
        self.assertEqual(mr.method_map['patch'], fake)
        self.assertEqual(mr.method_map['put'], fake)

    def test_call(self):
        """
        Tests whether calling an instance of MethodRouter
        properly dispatches an apimethod
        """
        dispatcher = mock.MagicMock()
        adapter = mock.MagicMock()
        adapter.formatted_body = 'some_body'
        adapter.extra_headers = {'some': 'header'}
        dispatcher.dispatch.return_value = adapter
        mr = MethodRouter(None, dispatcher)

        def fake():
            pass
        mr.add_route(endpoint_func=fake, methods=['GET', 'post'])

        request = mock.MagicMock()
        request.method = 'put'
        resp = mr(request)
        self.assertIsInstance(resp, HttpResponseNotAllowed)

        request.method = 'get'
        resp = mr(request)
        self.assertIsInstance(resp, HttpResponse)
        self.assertEqual(dispatcher.dispatch.call_count, 1)

        request.method = 'post'
        resp = mr(request)
        self.assertIsInstance(resp, HttpResponse)
        self.assertIsInstance(resp, HttpResponse)
        self.assertEqual(dispatcher.dispatch.call_count, 2)


    def test_method_map_property(self):
        """
        Simple test for the method_map property
        """
        self.assertIsNone(MethodRouter._method_map)
        mr = MethodRouter(None, None)
        self.assertEqual(mr.method_map, {})
        mr.method_map['key'] = 'value'
        self.assertDictEqual(mr.method_map, {'key': 'value'})
        self.assertIsNone(MethodRouter._method_map)

    def test_get_func_for_method(self):
        """
        tests the get_func_for_method
        """
        mr = MethodRouter(None, None)

        def fake():
            pass
        mr.add_route(endpoint_func=fake, methods=['GET', 'post'])

        def fake2():
            pass
        mr.add_route(endpoint_func=fake2, methods=['PATCH'])

        self.assertEqual(mr.get_func_for_method('GET'), fake)
        self.assertEqual(mr.get_func_for_method('get'), fake)

        self.assertEqual(mr.get_func_for_method('POST'), fake)
        self.assertEqual(mr.get_func_for_method('post'), fake)

        self.assertEqual(mr.get_func_for_method('PATCH'), fake2)
        self.assertEqual(mr.get_func_for_method('patch'), fake2)

        self.assertRaises(MethodNotAllowed, mr.get_func_for_method, 'PUT')
        self.assertRaises(MethodNotAllowed, mr.get_func_for_method, 'put')