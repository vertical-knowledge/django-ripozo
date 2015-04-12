from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime, time, date

from decimal import Decimal

from django.db.models.manager import Manager

from django_ripozo.manager import DjangoManager

from django_ripozo_tests.helpers.common import UnittestBase

from ripozo.exceptions import NotFoundException
from ripozo.viewsets.fields.common import StringField, BooleanField, FloatField, DateTimeField, IntegerField

from testapp.models import MyModel

import random
import string
import six
import unittest


def random_string():
    return ''.join(random.choice(string.ascii_letters) for _ in range(20))


def random_int():
    return random.choice(range(100))


def random_bool():
    return random.choice([True, False])


class TestDjangoManager(UnittestBase, unittest.TestCase):
    def setUp(self):
        class MyMangaer(DjangoManager):
            model = MyModel
            _fields = ['id', 'biginteger', 'boolean', 'char', 'csi',
                       'date_a', 'datetime_a', 'decimal_a',
                       'email', 'float_a', 'integer', 'ipaddress', 'genericip',
                       'nullbool', 'positiveint', 'positivesmallint', 'slug',
                       'smallint', 'time_a', 'url']

        self.model = MyModel
        self.manager = MyMangaer
        super(TestDjangoManager, self).setUp()

    def assertJsonifiedDict(self, d1, d2):
        for key, value in six.iteritems(d1):
            response_value = d2[key]
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
                response_value = response_value.strip('Z')
            elif isinstance(value, time):
                value = value.strftime('%H:%M:%S')
            elif isinstance(value, date):
                value = value.strftime('%Y-%m-%d')
            self.assertEqual(response_value, value)

    def create_model(self):
        values = self.get_fields_dict()
        model = self.model(**values)
        model.save()
        return dict(id=model.id), values

    @property
    def field_type_dict(self):
        return dict(id=IntegerField, biginteger=IntegerField, boolean=BooleanField,
                    char=StringField, csi=StringField, date_a=DateTimeField, datetime_a=DateTimeField,
                    decimal_a=StringField, email=StringField, float_a=FloatField,
                    integer=IntegerField, ipaddress=StringField, genericip=StringField,
                    nullbool=BooleanField, positiveint=IntegerField, positivesmallint=IntegerField,
                    slug=StringField, smallint=IntegerField, time_a=DateTimeField, url=StringField)

    def get_fields_dict(self):
        return dict(
            biginteger=random_int(),
            boolean=random_bool(),
            char=random_string(),
            csi=random_string(),
            date_a=date.today(),
            datetime_a=datetime.utcnow(),
            decimal_a='1.02',
            # duration=datetime.now(),
            email=random_string(),
            float_a=1.02,
            integer=random_int(),
            ipaddress=random_string(),
            genericip=random_string(),
            nullbool=random_bool(),
            positiveint=random_int(),
            positivesmallint=random_int(),
            slug=random_string(),
            smallint=random_int(),
            time_a=time(),
            url=random_string()
        )

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
        self.assertJsonifiedDict(value, response)
        for f in self.manager.fields:
            self.assertIn(f, response)

    def test_retrieve(self):
        """
        Tests retrieving an existing model
        """
        lookup_keys, values = self.create_model()
        values.update(lookup_keys)
        response = self.manager().retrieve(lookup_keys)
        self.assertJsonifiedDict(values, response)

    def test_retrieve_404(self):
        """
        Tests retrieving a model that does not
        exist.
        """
        self.assertRaises(NotFoundException, self.manager().retrieve, dict(id=1040230))

    def test_retrieve_all(self):
        """
        Tests the retrieval of all available objects.
        """
        vals, meta = self.manager().retrieve_list({})
        original_length = len(vals)

        new_count = 100
        all_vals = []
        for i in range(new_count):
            lookup, indv_vals = self.create_model()
            indv_vals.update(lookup)
            all_vals.append(indv_vals)
        vals, meta = self.manager().retrieve_list({})
        self.assertEqual(len(vals), original_length + new_count)

    def test_pagination(self):
        """
        Test retrieve_list with pagination.
        """
        class NewManager(self.manager):
            paginate_by = 3

        vals, meta = self.manager().retrieve_list({})
        original_length = len(vals)

        new_count = 100
        for i in range(new_count):
            self.create_model()

        vals, meta = NewManager().retrieve_list({})
        total_retrieved = len(vals)
        while 'next' in meta['links']:
            vals, meta = NewManager().retrieve_list({
                NewManager.pagination_count_query_arg: meta['links']['next'][NewManager.pagination_count_query_arg],
                NewManager.pagination_pk_query_arg: meta['links']['next'][NewManager.pagination_pk_query_arg]
            })
            total_retrieved += len(vals)
            self.assertLessEqual(len(vals), NewManager.paginate_by)
        self.assertEqual(original_length + new_count, total_retrieved)

    def test_list_fields_retrieve_all(self):
        """
        Checks to ensure that the list fields are used if
        they are available.
        """
        assert False

    def test_update(self):
        """
        Simple check for updating.
        """
        lookup, values = self.create_model()
        new_vals = self.get_fields_dict()
        vals = self.manager().update(lookup, new_vals)
        model = self.manager().get_model(lookup)
        for key, val in six.iteritems(new_vals):
            model_val = getattr(model, key)
            if isinstance(model_val, Decimal):
                model_val = six.text_type(model_val)
            self.assertEqual(model_val, val)

    def test_update_not_existing(self):
        """
        Tests attempting to update an object that does not exist.
        """
        self.assertRaises(NotFoundException, self.manager().update, {'id': -1}, {'hehe': 1})

    def test_delete(self):
        """
        Tests simple delete
        """
        lookup, vals = self.create_model()
        self.manager().delete(lookup)
        self.assertRaises(NotFoundException, self.manager().get_model, lookup)

    def test_delete_not_existing(self):
        """
        Tests the deletion of a resource that
        does not exist.
        """
        self.assertRaises(NotFoundException, self.manager().delete, {'id': -1})