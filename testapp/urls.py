from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django_ripozo.dispatcher import DjangoDispatcher

from ripozo.dispatch.adapters import SirenAdapter, HalAdapter

from testapp.resources import HelloResource, HelloWorldIdResource


dispatcher = DjangoDispatcher(base_url='/api')
dispatcher.register_resources(HelloResource, HelloWorldIdResource)
dispatcher.register_adapters(SirenAdapter, HalAdapter)

urlpatterns = dispatcher.url_patterns