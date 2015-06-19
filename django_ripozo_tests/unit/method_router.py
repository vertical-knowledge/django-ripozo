from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.http import HttpResponseNotAllowed, HttpResponse

from django_ripozo.dispatcher import MethodRouter, default_error_handler
from django_ripozo.exceptions import MethodNotAllowed

from django_ripozo_tests.helpers.common import UnittestBase

from ripozo.adapters import SirenAdapter
from ripozo.exceptions import RestException

import django
import mock
import six
import unittest2


class TestMethodRouter(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            django.setup()
        except AttributeError:
            pass

    def test_default_error_handler(self):
        """
        Tests in the case of a RestException
        """
        re = RestException('blah', status_code=499)
        resp = default_error_handler(None, None, SirenAdapter, re)
        self.assertIsInstance(resp, HttpResponse)
        self.assertEqual(resp.status_code, 499)

    def test_default_error_handler_non_ripozo(self):
        """
        Tests in the case of an unknown exception.
        """
        e = ValueError('blah')
        self.assertRaises(ValueError, default_error_handler, None, None, None, e)

    def test_add_route_casing(self):
        """
        Tests that the appropriate case (lower)
        case is always implicitly forced.
        """
        mr = MethodRouter(None, None)
        methods = ('FIRST', 'Second', 'thIrd', 'fourth')
        mr.add_route(endpoint_func=1, methods=methods)
        for m in mr.method_map.keys():
            self.assertTrue(m.islower())

    def test_add_route_value_error(self):
        """
        Tests that a value error is raised if
        the same method is already in the method router.
        """
        mr = MethodRouter(None, None)
        methods = ('FIRST', 'first')
        self.assertRaises(ValueError, mr.add_route, endpoint_func=1, methods=methods)

    def test_method_map_property(self):
        mr = MethodRouter(None, None)
        self.assertDictEqual(mr.method_map, {})

    def test_get_func_for_method_available(self):
        """
        Tests that the get_func_for_method works appropriately
        """
        mr = MethodRouter(None, None)
        mr.add_route(endpoint_func=1, methods=['GET'])
        self.assertEqual(mr.get_func_for_method('GET'), 1)

    def test_get_func_for_method_unavailable(self):
        """
        Tests that the get_func_for_method works appropriately
        """
        mr = MethodRouter(None, None)
        self.assertRaises(MethodNotAllowed, mr.get_func_for_method, 'GET')

    def test_call_normal_case(self):
        """
        Tests calling the method router under normal case.
        """
        dispatcher = mock.MagicMock()
        adapter = mock.Mock(formatted_body='some_body', extra_headers={'some': 'header'}, status_code=42)
        dispatcher.dispatch.return_value = adapter
        mr = MethodRouter(None, dispatcher)
        mr.add_route(endpoint_func=mock.MagicMock(), methods=['GET', 'post'])
        request = mock.MagicMock(method='get')
        resp = mr(request)
        self.assertIsInstance(resp, HttpResponse)
        self.assertEqual(resp.content.decode(), 'some_body')
        self.assertEqual(resp.status_code, 42)

    def test_call_exception_handler(self):
        dispatcher = mock.MagicMock()
        adapter = mock.Mock(formatted_body='some_body', extra_headers={'some': 'header'}, status_code=42)
        dispatcher.dispatch.return_value = adapter
        error_handler = mock.MagicMock()
        mr = MethodRouter(None, dispatcher, error_handler=error_handler)
        mr.add_route(endpoint_func=mock.MagicMock(), methods=['GET', 'post'])
        request = mock.MagicMock(method='put')
        resp = mr(request)
        self.assertEqual(error_handler.call_count, 1)
