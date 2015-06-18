from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__author__ = 'Tim Martin'

from django.http import HttpResponseNotAllowed, HttpResponse, QueryDict
from django.conf.urls import url

from django_ripozo.exceptions import MethodNotAllowed

from functools import wraps

from ripozo.dispatch.dispatch_base import DispatcherBase
from ripozo.exceptions import RestException
from ripozo.resources.request import RequestContainer
from ripozo.utilities import join_url_parts

import re
import six

def _csrf_wrapper(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return f(*args, **kwargs)
    wrapped.csrf_exempt = True
    return wrapped


def default_error_handler(dispatcher, request, adapter_class, exc):
    """
    The default error handler used by the method router
    when there is an error in the application.  This provides
    a convienent place to appropriately handle exceptions.
    Perhaps just reraising all exceptions.

    :param DjangoDispatcher dispatcher: The dispatcher that
        was used to dispatch this method.  Not used by
        this handler.
    :param ripozo.RequestContainer request: The request that
        caused the exception.  Not used by this handler.
    :param ripozo.AdapterBase adapter_class: The adapter
    :param Exception exc:
    :return: The correctly formatted status.
    :rtype: HttpResponse
    """
    if isinstance(exc, RestException):
        body, content_type, status_code = adapter_class.format_exception(exc)
        return HttpResponse(body, status=status_code, content_type=content_type)
    raise exc


class MethodRouter(object):
    """
    This is a callable object that is responsible
    for calling the specific method responsible for
    handling the http verb that was used.  This is because
    Django does not have a manner of directing different
    HTTP verbs to different methods.
    """
    _method_map = None

    def __init__(self, route, dispatcher, error_handler=default_error_handler):
        """
        :param unicode route:
        :param DjangoDispatcher dispatcher:
        :param function error_handler: A function that takes the dispatcher,
            request, adapter base class, and an exception that was raised when
            dispatching the request.
        :return:
        :rtype:
        """
        self.route = route
        self.dispatcher = dispatcher
        self.error_handler = error_handler

    def add_route(self, endpoint_func=None, endpoint=None, methods=None, **options):
        """
        Adds a function to call and the http methods that will
        correspond to it.  Currently, the endpoint and options are ignored.

        :param function endpoint_func: The function to be called when the route
            is called with one of the methods specified.
        :param unicode endpoint: Not used currently
        :param list methods: A list of the unicode methods that
            correspond to the endpoint_func.  They are case insensitive.
        :param dict options: Not used currently.
        """
        for method in methods:
            method = method.lower()
            if method in self.method_map:
                raise ValueError('The method {0} is already registered for the route '
                                 '{1}'.format(method, self.route))
            self.method_map[method.lower()] = endpoint_func

    @_csrf_wrapper
    def __call__(self, django_request, **url_parameters):
        """
        This is a call to a django method.

        :param django.http.HttpRequest django_request: The django
            request object.
        :param dict url_parameters: The named url parameters
        :return: The django HttpResponse
        :rtype: django.http.HttpResponse
        """
        accepted_mimetypes = django_request.META.get('HTTP_ACCEPT', [])
        adapter_class = self.dispatcher.get_adapter_for_type(accepted_mimetypes)
        body_parameters = QueryDict(django_request.body)
        request = DjangoRequestContainer(django_request, url_params=url_parameters,
                                         query_args=dict(django_request.GET), body_args=dict(body_parameters),
                                         headers=dict(django_request.META))
        try:
            endpoint_func = self.get_func_for_method(django_request.method)
            adapter = self.dispatcher.dispatch(endpoint_func, accepted_mimetypes, request)
        except Exception as e:
            return self.error_handler(self.dispatcher, request, adapter_class, e)
        response = HttpResponse(adapter.formatted_body, status=adapter.status_code)
        for header, value in six.iteritems(adapter.extra_headers):
            response[header] = value
        return response

    @property
    def method_map(self):
        """
        :return: The dictionary of the HTTP methods
            and their corresponding endpoint functions.
        :rtype: dict
        """
        if self._method_map is None:
            self._method_map = {}
        return self._method_map

    def get_func_for_method(self, http_method):
        """
        :param unicode http_method: The http verb
        :return: The method corresponding to the http verb
        :rtype: types.MethodType
        """
        http_method = http_method.lower()
        try:
            return self.method_map[http_method]
        except KeyError:
            raise MethodNotAllowed('The method {0} is not available for '
                                   'the route {1}'.format(http_method, self.route))

_url_parameter_finder = re.compile(r'<(.+?)>')


class DjangoDispatcher(DispatcherBase):
    # TODO docs
    _url_map = None
    _routers = None

    def __init__(self, base_url='', method_route_class=MethodRouter, error_handler=default_error_handler):
        self._base_url = base_url
        self.method_route_class = method_route_class
        self.error_handler = error_handler

    @property
    def url_map(self):
        """
        :return: A dictionary of the unicode routes and
            the MethodRouters that correspond to that route.
        :rtype: dict
        """
        if self._url_map is None:
            self._url_map = {}
        return self._url_map

    @property
    def base_url(self):
        """
        :return: The base part of the url that will
            be prepended to all routes.  For example,
            you might use '/api' to dictate what every
            url should be prepended with.
        :rtype: unicode
        """
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
        route = join_url_parts(self.base_url, route)
        route = self._convert_url_to_regex(route)
        if route not in self.url_map:
            self.url_map[route] = self.method_route_class(route, self, self.error_handler)
        method_router = self.url_map[route]
        method_router.add_route(endpoint_func=endpoint_func, endpoint=endpoint,
                                methods=methods, **options)

    @property
    def url_patterns(self):
        """
        :return: A list of tuples built according to the
            ``django.conf.urls.patterns`` method.  The
            first argument is the base_url that will
            be prepended.
        :rtype: list
        """
        urls = []
        for router in six.itervalues(self.url_map):
            urls.append(url(router.route, router))
        return urls

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

    def dispatch(self, endpoint_func, accepted_mimetypes, *args, **kwargs):
        """
        A helper to dispatch the endpoint_func, get the ResourceBase
        subclass instance, get the appropriate AdapterBase subclass
        and return an instance created with the ResourceBase.

        :param method endpoint_func: The endpoint_func is responsible
            for actually get the ResourceBase response
        :param list accepted_mimetypes: The mime types accepted by
            the client.  If none of the mimetypes provided are
            available the default adapter will be used.
        :param list args: a list of args that wll be passed
            to the endpoint_func
        :param dict kwargs: a dictionary of keyword args to
            pass to the endpoint_func
        :return: an instance of an AdapterBase subclass that
            can be used to find
        :rtype:
        """
        result = endpoint_func(*args, **kwargs)
        request = args[0]
        base_url = request.django_request.build_absolute_uri(self.base_url)
        adapter_class = self.get_adapter_for_type(accepted_mimetypes)
        adapter = adapter_class(result, base_url=base_url)
        return adapter


class DjangoRequestContainer(RequestContainer):
    def __init__(self, request, *args, **kwargs):
        self.django_request = request
        super(DjangoRequestContainer, self).__init__(*args, **kwargs)