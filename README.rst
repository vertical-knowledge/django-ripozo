django-ripozo
=============

.. image:: https://travis-ci.org/vertical-knowledge/django-ripozo.svg?branch=master&style=flat
    :target: https://travis-ci.org/vertical-knowledge/django-ripozo
    :alt: test status

.. image:: https://coveralls.io/repos/vertical-knowledge/django-ripozo/badge.svg?branch=master&style=flat
    :target: https://coveralls.io/r/vertical-knowledge/django-ripozo?branch=master
    :alt: test coverage

.. image:: https://readthedocs.org/projects/django-ripozo/badge/?version=latest&style=flat
    :target: https://django-ripozo.readthedocs.org/
    :alt: documentation status

Integrates ripozo with django for fast, flexible 
Hypermedia, HATEOAS, and other REST apis.

`Full django-ripozo documentation <http://django-ripozo.readthedocs.org/>`_

Looking for the `ripozo documentation? <http://ripozo.readthedocs.org/>`_

Minimal App
-----------

You'll need to instantiate the django project in
the standard manner.  If you aren't sure how to
do this, check out the excellent
`django documentation.<https://docs.djangoproject.com/en/1.8/intro/tutorial01/>`_

In your app you'll need a resources.py file.

.. code-block:: python

    from ripozo import ResourceBase, apimethod

    class MyResource(ResourceBase):
        @apimethod(methods=['GET'])
        def say_hello(cls, request):
            return cls(properties=dict(hello='world'))

And in your urls.py file

.. code-block:: python

    from ripozo.adapters import SirenAdapter, HalAdapter
    from .resources import MyResource

    dispatcher = DjangoDispatcher()
    dispatcher.register_resources(MyResource)
    dispatcher.register_adapters(SirenAdapter, HalAdapter)

    urlpatterns = dispatcher.url_patterns

And just like that you have a fully functional application.

Looking for a more extensive example?
Check out an `example<http://django-ripozo.readthedocs.org/en/latest/tutorial/setup.html>`_
with database interactions as well.
