from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django_ripozo.easy_resources import _get_pks, _get_fields_for_model, _get_relationships
import unittest2

from testapp.models import OneToMany, ManyToOne, MyModel


class TestEasyResource(unittest2.TestCase):
    def test_get_pks(self):
        resp = _get_pks(MyModel)
        self.assertTupleEqual(('id',), resp)
