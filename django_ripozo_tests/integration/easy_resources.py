from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ripozo.resources.relationships import Relationship, ListRelationship

from django_ripozo.easy_resources import _get_pks, _get_fields_for_model, \
    _get_relationships, create_resource
import unittest2

from testapp.models import OneToMany, ManyToOne, MyModel, ManyToManyFirst, \
    ManyToManySecond, OneFirst, OneSecond


class TestEasyResource(unittest2.TestCase):
    def test_get_pks(self):
        resp = _get_pks(MyModel)
        self.assertTupleEqual(('id',), resp)

    def test_get_fields(self):
        resp = _get_fields_for_model(OneToMany)
        self.assertEqual(set(resp), set(['id', 'one_value', 'manies.id']))

    def test_get_relationships_one_to_many(self):
        resp = _get_relationships(OneToMany)
        self.assertEqual(len(resp), 1)
        self.assertIsInstance(resp, tuple)
        rel = resp[0]
        self.assertEqual(rel.name, 'manies')
        self.assertEqual(rel._relation, 'ManyToOne')
        self.assertIsInstance(rel, ListRelationship)

    def test_get_relationships_many_to_one(self):
        resp = _get_relationships(ManyToOne)
        self.assertEqual(len(resp), 1)
        self.assertIsInstance(resp, tuple)
        rel = resp[0]
        self.assertEqual(rel.name, 'one')
        self.assertEqual(rel._relation, 'OneToMany')
        self.assertIsInstance(rel, Relationship)

    def test_create_resource(self):
        res = create_resource(OneToMany)
        self.assertEqual(len(res._relationships), 1)
        self.assertEqual(res.resource_name, 'one_to_many')
        self.assertTupleEqual(res.pks, ('id',))
        res2 = create_resource(ManyToOne)
        self.assertEqual(len(res2._relationships), 1)
        self.assertEqual(res2.resource_name, 'many_to_one')
        self.assertTupleEqual(res2.pks, ('id',))

    def test_get_relationships_many_to_many_implicit(self):
        resp = _get_relationships(ManyToManyFirst)
        self.assertEqual(len(resp), 1)
        self.assertIsInstance(resp, tuple)
        rel = resp[0]
        self.assertEqual(rel.name, 'all_the_manies')
        self.assertEqual(rel._relation, 'ManyToManySecond')
        self.assertIsInstance(rel, ListRelationship)

    def test_get_relationships_many_to_many_explicit(self):
        resp = _get_relationships(ManyToManySecond)
        self.assertEqual(len(resp), 1)
        self.assertIsInstance(resp, tuple)
        rel = resp[0]
        self.assertEqual(rel.name, 'many_to_many')
        self.assertEqual(rel._relation, 'ManyToManyFirst')
        self.assertIsInstance(rel, ListRelationship)

    def test_get_relationships_one_to_one_implicit(self):
        resp = _get_relationships(OneFirst)
        self.assertEqual(len(resp), 1)
        self.assertIsInstance(resp, tuple)
        rel = resp[0]
        self.assertEqual(rel.name, 'second')
        self.assertEqual(rel._relation, 'OneSecond')
        self.assertIsInstance(rel, Relationship)

    def test_get_relationships_one_to_one_explicit(self):
        resp = _get_relationships(OneSecond)
        self.assertEqual(len(resp), 1)
        self.assertIsInstance(resp, tuple)
        rel = resp[0]
        self.assertEqual(rel.name, 'first')
        self.assertEqual(rel._relation, 'OneFirst')
        self.assertIsInstance(rel, Relationship)

