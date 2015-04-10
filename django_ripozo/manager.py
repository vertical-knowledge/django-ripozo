from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.core import serializers
from django.db import models

from ripozo.managers.base import BaseManager
from ripozo.viewsets.fields.common import BaseField, StringField, \
    BooleanField, FloatField, DateTimeField, IntegerField

import json
import six


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
                                 models.IPAddressField, models.UUIDField, models.DecimalField)):
            return StringField(name)
        elif isinstance(column, (models.DateTimeField, models.DateField, models.TimeField, models.DurationField)):
            return DateTimeField(name)
        elif isinstance(column, (models.BooleanField, models.NullBooleanField,)):
            return BooleanField(name)
        elif isinstance(column, models.FloatField):
            return FloatField(name)
        else:
            return BaseField(name)

    def create(self, values, *args, **kwargs):
        """
        Creates a new model using the values provided.
        *args and **kwargs are ignored.

        :param dict values: A dictionary of the values to set
            on the new model that is being created
        :param list args: Ignored for now
        :param dict kwargs: Ignored for now
        :return: The new properties on the model,
            including the items on the model that are
            defaults
        :rtype: dict
        """
        model = self.model()
        model = self._set_fields_on_model(model, values)
        model.save()
        return self.serialize_model(model)

    def retrieve(self, lookup_keys, *args, **kwargs):
        """
        Gets a model and selects the fields from the fields
        attribute on this manager to return in a dict.

        :param dict lookup_keys: The keys used to find the model
            to serialize
        :return: The serialized model in a dictionary form with just
            the fields specified in the manager.
        :rtype: dict
        """
        model = self.queryset.filter(**lookup_keys).get()
        return self.serialize_model(model)

    def retrieve_list(self, filters, *args, **kwargs):
        pass

    def update(self, lookup_keys, updates, *args, **kwargs):
        pass

    def delete(self, lookup_keys, *args, **kwargs):
        pass

    def serialize_model(self, model):
        """
        :param model: The model that is being serialized.
        :type model: django.db.models.Model
        :return: The serialized model
        :rtype: dict
        """
        data = serializers.serialize('json', [model], fields=self.fields)
        data = json.loads(data)[0]['fields']
        if 'id' in self.fields:
            data['id'] = model.id
        if 'pk' in self.fields:
            data['pk'] = model.pk
        return data

    def _set_fields_on_model(self, model, values):
        """
        Will set the values on the model if and only
        if they are present in the fields property.
        If they are not it will silently skip them.

        :param model:
        :type model: django.db.models.Model
        :param dict values:
        :return: The updated model
        :rtype: django.db.models.Model
        """
        for name, value in six.iteritems(values):
            if name in self.fields:
                setattr(model, name, value)
        return model