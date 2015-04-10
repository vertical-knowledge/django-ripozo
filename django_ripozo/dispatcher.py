from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__author__ = 'Tim Martin'

from django.http import HttpResponseNotAllowed, HttpResponse
from django.conf.urls import patterns, url

from django_ripozo.exceptions import MethodNotAllowed

from ripozo.dispatch.dispatch_base import DispatcherBase
from ripozo.viewsets.request import RequestContainer

import re
import six

_url_parameter_finder = re.compile(r'<(.+?)>')


class DjangoDispatcher(DispatcherBase):
    # TODO docs/test
    _url_map = None
    _routers = None

    def __init__(self, base_url=''):
        self._base_url = base_url

    @property
    def routers(self):
        if self._routers is None:
            self._routers = {}
        return self._routers

    @property
    def url_map(self):
        if self._url_map is None:
            self._url_map = {}
        return self._url_map

    @property
    def base_url(self):
        return self._base_url

    def register_route(self, endpoint, endpoint_func=None, route=None, methods=None, **options):
        """
        Adds a route to the url_map which is used when getting
        the url_patterns property which are then added to the django
        app.

        :param unicode endpoint: The name of this endpoint
        :param function endpoint_func: the function that should be called when
            this endpoint is hit.
        :param unicode route: The url that corresponds to this endpoint.
            Each unique url generates a MethodRouter which then dispatches
            them to the appopriate endpoints for the http verbs
        :param list methods: The http verbs that correspond to this endpoint
        :param dict options: Additional options.  Not used at this time
        """
        route = self._convert_url_to_regex(route)
        if route not in self.url_map:
            self.url_map[route] = MethodRouter(route, self)
        method_router = self.url_map[route]
        method_router.add_route(endpoint_func=endpoint_func, endpoint=endpoint,
                                methods=methods, **options)

    @property
    def url_patterns(self):
        urls = []
        for router in six.itervalues(self.url_map):
            urls.append(url(router.route, router))
        return patterns(self.base_url, *urls)


    @staticmethod
    def _convert_url_to_regex(route):
        """
        Takes a ripozo formatted url (one with the url
        parameters enclosed in angle brackets such as ``'/myresource/<id>/'``)
        and returns a django regex formatted url: '^myresource/(?P<id>[^/]+)/$'.
        It will also append the ^ character to the beggining and $ character
        to the end.

        :param unicode route:
        :return: A django formatted url regex pattern.
        :rtype: unicode
        """
        url_parameters = set(_url_parameter_finder.findall(route))
        for param in url_parameters:
            old_param = '<{0}>'.format(param)
            new_param = '(?P<{0}>[^/]+)'.format(param)
            route = route.replace(old_param, new_param)
        route = route.lstrip('/')
        return '^{0}$'.format(route)

class DjangoRequestContainer(RequestContainer):
    def __init__(self, request, *args, **kwargs):
        self.django_request = request
        super(DjangoRequestContainer, self).__init__(*args, **kwargs)


class MethodRouter(object):
    _method_map = None

    def __init__(self, route, dispatcher):
        self.route = route
        self.dispatcher = dispatcher

    def add_route(self, endpoint_func=None, endpoint=None, methods=None, **options):
        for method in methods:
            method = method.lower()
            if method in self.method_map:
                raise ValueError('The method {0} is already registered for the route '
                                 '{1}'.format(method, self.route))
            self.method_map[method.lower()] = endpoint_func

    def __call__(self, django_request, **url_parameters):
        try:
            endpoint_func = self.get_func_for_method(django_request.method)
        except MethodNotAllowed as e:
            return HttpResponseNotAllowed(six.iterkeys(self.method_map))
        request = DjangoRequestContainer(django_request, url_params=url_parameters,
                                         query_args=django_request.GET, body_args=django_request.POST,
                                         headers=django_request.META)
        adapter = self.dispatcher.dispatch(endpoint_func, request.content_type, request)
        response = HttpResponse(adapter.formatted_body)
        for header, value in six.iteritems(adapter.extra_headers):
            response[header] = value
        return response


    @property
    def method_map(self):
        if self._method_map is None:
            self._method_map = {}
        return self._method_map

    def get_func_for_method(self, http_method):
        """

        :param unicode method:
        :return:
        :rtype: types.MethodType
        """
        http_method = http_method.lower()
        if http_method not in self.method_map:
            raise MethodNotAllowed('The method {0} is not available for '
                                   'the route {1}'.format(http_method, self.route))
        return self.method_map[http_method]