from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime
import random
import string
import unittest
import uuid

from django.db.models.manager import Manager
from ripozo.viewsets.fields.common import StringField, BooleanField, FloatField, DateTimeField, IntegerField
import six

from django_ripozo.manager import DjangoManager
from django_ripozo_tests.helpers.common import UnittestBase
from testapp.models import MyModel


def random_string():
    return ''.join(random.choice(string.letters) for _ in range(20))


def random_int():
    return random.choice(range(100))


def random_bool():
    return random.choice([True, False])


class TestDjangoManager(UnittestBase, unittest.TestCase):
    def setUp(self):
        class MyMangaer(DjangoManager):
            model = MyModel
            _fields = ['id', 'biginteger', 'boolean', 'char', 'csi',
                       'date_', 'datetime_', 'decimal_',
                       'email', 'float_', 'integer', 'ipaddress', 'genericip',
                       'nullbool', 'positiveint', 'positivesmallint', 'slug',
                       'smallint', 'time_', 'url', 'uuid']

        self.model = MyModel
        self.manager = MyMangaer
        super(TestDjangoManager, self).setUp()

    @property
    def field_type_dict(self):
        return dict(id=IntegerField, biginteger=IntegerField, boolean=BooleanField,
                    char=StringField, csi=StringField, date_=DateTimeField, datetime_=DateTimeField,
                    decimal_=FloatField, email=StringField, float_=FloatField,
                    integer=IntegerField, ipaddress=StringField, genericip=StringField,
                    nullbool=BooleanField, positiveint=IntegerField, positivesmallint=IntegerField,
                    slug=StringField, smallint=IntegerField, time_=DateTimeField, url=StringField,
                    uuid=StringField)

    def get_fields_dict(self):
        return dict(
            id=random_int(),
            biginteger=random_int(),
            boolean=random_bool(),
            char=random_string(),
            csi=random_string(),
            date_=datetime.now(),
            datetime_=datetime.now(),
            decimal_=1.02,
            # duration=datetime.now(),
            email=random_string(),
            float_=1.02,
            integer=random_int(),
            ipaddress=random_string(),
            genericip=random_string(),
            nullbool=random_bool(),
            positiveint=random_int(),
            positivesmallint=random_int(),
            slug=random_string(),
            smallint=random_int(),
            time_=datetime.now(),
            url=random_string(),
            uuid=six.text_type(uuid.uuid1()))

    def test_queryset_property(self):
        """
        Tests the queryset property on the DjangoManager
        pretty basic
        """
        queryset = self.manager().queryset
        self.assertIsInstance(queryset, Manager)

        class FakeManager(DjangoManager):
            pass

        try:
            FakeManager().queryset
            assert False
        except AttributeError:
            pass

    def test_get_field_type(self):
        """
        Tests whether the appropriate field type is returned.
        """
        for name, value in six.iteritems(self.field_type_dict):
            self.assertIsInstance(self.manager().get_field_type(name), value,
                                  msg='{0} does not return {1}'.format(name, value))

    def test_create(self):
        """
        Tests the creation of an object using the serializer.
        """
        m = self.manager()
        value = self.get_fields_dict()
        response = m.create(value)
        for key, value in six.iteritems(value):
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
            self.assertEqual(response[key], value)