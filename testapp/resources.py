from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ripozo.decorators import apimethod
from ripozo.viewsets.resource_base import ResourceBase


class HelloResource(ResourceBase):
    _resource_name = 'myresource'

    @apimethod(methods=['GET'])
    def say_hello(cls, request, *args, **kwargs):
        return cls(properties=dict(hello='world'))


class HelloWorldIdResource(ResourceBase):
    _resource_name = 'myidresource'
    _pks = ['id']

    @apimethod(methods=['GET'])
    def say_hello(cls, request, *args, **kwargs):
        return cls(properties=dict(hello='world', id=request.url_params['id']))
