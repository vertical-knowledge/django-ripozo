from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.db import models
from django.db.models.manager import Manager

from django_ripozo.manager import DjangoManager

from django_ripozo_tests.helpers.common import UnittestBase

import unittest


class TestDjangoManager(UnittestBase, unittest.TestCase):
    def setUp(self):
        class MyModel(models.Model):
            """
            Doesn't include relationships or files for now
            """
            biginteger = models.BigIntegerField()
            boolean = models.BooleanField()
            char = models.CharField(max_length=100)
            csi = models.CommaSeparatedIntegerField(max_length=100)
            date_ = models.DateField()
            datetime_ = models.DateTimeField()
            decimal_ = models.DecimalField(max_digits=5, decimal_places=2)
            duration = models.DurationField()
            email = models.EmailField()
            float_ = models.FloatField()
            integer = models.IntegerField()
            ipaddress = models.IPAddressField()
            genericip = models.GenericIPAddressField()
            nullbool = models.NullBooleanField()
            positiveint = models.PositiveIntegerField()
            positivesmallint = models.PositiveSmallIntegerField()
            slug = models.SlugField()
            smallint = models.SmallIntegerField()
            time_ = models.TimeField()
            url = models.URLField()
            uuid = models.UUIDField()

        class MyMangaer(DjangoManager):
            model = MyModel
            _fields = ['id', 'biginteger', 'boolean', 'char', 'csi',
                       'date_', 'datetime_', 'decimal_', 'duration',
                       'email', 'float_', 'integer', 'ipaddress', 'genericip',
                       'nullbool', 'positiveint', 'positivesmallint', 'slug',
                       'smallint', 'time_', 'url', 'uuid']

        self.model = MyModel
        self.manager = MyMangaer

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

    def test_