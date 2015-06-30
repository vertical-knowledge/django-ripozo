from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django_ripozo.manager import DjangoManager

from django_ripozo_tests.helpers.common import UnittestBase, random_string

from testapp.models import OneToMany, ManyToOne

import unittest2


class TestDjangoManager(UnittestBase, unittest2.TestCase):
    def setUp(self):
        class OneManager(DjangoManager):
            model = OneToMany
            fields = ['id', 'one_value', 'manies.id', 'manies.many_value']

        class ManyManager(DjangoManager):
            # TODO Test one creation
            model = ManyToOne
            fields = ['id', 'many_value', 'one_id']

        self.one = OneManager()
        self.many = ManyManager()

    def create_one(self, one_value=None):
        one_value = one_value or random_string()
        return OneToMany.objects.create(one_value=one_value)

    def create_many(self, many_value=None, one=None):
        one = one or self.create_one()
        many_value = many_value or random_string()
        return ManyToOne.objects.create(many_value=many_value, one=one)

    def test_create_one(self):
        val = random_string()
        resp = self.one.create(dict(one_value=val))
        id_ = resp.get('id')
        model = OneToMany.objects.get(id=id_)
        self.assertEqual(val, model.one_value)

    def test_create_many(self):
        one = self.create_one()
        resp = self.many.create(dict(many_value='something', one_id=one.id))
        many = ManyToOne.objects.get(id=resp.get('id'))
        self.assertIn(many, one.manies.all())

    def test_retrieve_one(self):
        one = self.create_one()
        many1 = self.create_many(one=one)
        many2 = self.create_many(one=one)
        resp = self.one.retrieve(dict(id=one.id))
        self.assertEqual(one.one_value, resp['one_value'])
        self.assertEqual(one.id, resp['id'])
        self.assertEqual(len(resp['manies']), 2)
        self.assertIsInstance(resp['manies'], list)
        found1 = found2 = False
        for m in resp['manies']:
            if m['id'] == many1.id:
                self.assertEqual(m['many_value'], many1.many_value)
                found1 = True
            elif m['id'] == many2.id:
                self.assertEqual(m['many_value'], many2.many_value)
                found2 = True
        self.assertTrue(found1 == found2 == True)

