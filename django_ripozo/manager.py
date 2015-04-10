from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.db import models

from ripozo.managers.base import BaseManager
from ripozo.viewsets.fields.common import BaseField, StringField, ListField, \
    BooleanField, FloatField, DateTimeField, IntegerField


class DjangoManager(BaseManager):
    """
    :param model: The django database model that this manager
        is responsible for handling
    :type model: django.db.models.Model
    """

    @property
    def queryset(self):
        """
        By default returns the self.model.objects
        If you wish to restrict the records available
        override this.
        """
        return self.model.objects

    def get_field_type(self, name):
        """
        :param unicode name: The name of the field to get the
            ripozo field type from.
        :return: The ripozo field type that most closely
            matches the database type.
        :rtype: ripozo.viewsets.fields.base.BaseField
        """
        column = self.model._meta._forward_fields_map[name]
        if isinstance(column, (models.IntegerField, models.AutoField)):
            return IntegerField(name)
        elif isinstance(column, (models.CharField, models.GenericIPAddressField,
                                 models.IPAddressField, models.UUIDField)):
            return StringField(name)
        elif isinstance(column, (models.DateTimeField, models.DateField, models.TimeField, models.DurationField)):
            return DateTimeField(name)
        elif isinstance(column, (models.BooleanField, models.NullBooleanField,)):
            return BooleanField(name)
        elif isinstance(column, (models.FloatField, models.DecimalField)):
            return FloatField(name)

    def create(self, values, *args, **kwargs):
        pass

    def retrieve(self, lookup_keys, *args, **kwargs):
        pass

    def retrieve_list(self, filters, *args, **kwargs):
        pass

    def update(self, lookup_keys, updates, *args, **kwargs):
        pass

    def delete(self, lookup_keys, *args, **kwargs):
        pass
