from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime, date, time, timedelta

from decimal import Decimal

from django.db import models
from django.db.models.query import QuerySet

from ripozo.exceptions import NotFoundException
from ripozo.managers.base import BaseManager
from ripozo.viewsets.fields.common import BaseField, StringField, \
    BooleanField, FloatField, DateTimeField, IntegerField

import logging
import six

logger = logging.getLogger(__name__)


def sql_to_json_encoder(obj):
    # TODO docs and test
    if isinstance(obj, dict):
        for key, value in six.iteritems(obj):
            obj[key] = sql_to_json_encoder(value)
    elif isinstance(obj, list):
        values = []
        for val in obj:
            values.append(sql_to_json_encoder(val))
        obj = values
    elif isinstance(obj, (datetime, date, time, timedelta)):
        obj = six.text_type(obj)
    elif isinstance(obj, Decimal):
        obj = float(obj)
    return obj


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
        column = self.model._meta.get_field_by_name(name)[0]
        if isinstance(column, (models.IntegerField, models.AutoField)):
            return IntegerField(name)
        elif isinstance(column, (models.CharField, models.GenericIPAddressField,
                                 models.IPAddressField, models.DecimalField)):
            return StringField(name)
        elif isinstance(column, (models.DateTimeField, models.DateField, models.TimeField)):
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
        model = self.get_model(lookup_keys)
        return self.serialize_model(model)

    def retrieve_list(self, filters, *args, **kwargs):
        """
        Retrieves a list of records.

        :param dict filters:
        :return:
        :rtype:
        """
        count = filters.pop(self.pagination_count_query_arg, self.paginate_by)
        page = filters.pop(self.pagination_pk_query_arg, 0)

        offset = page * count
        total = self.queryset.filter(**filters).count()
        queryset = self.queryset.filter(**filters)[offset:offset + count]

        prev_page = None
        next_page = None
        if total > offset + count:
            next_page = page + 1
        if page > 0:
            prev_page = page - 1
        links = dict()
        if prev_page:
            links.update(dict(prev={self.pagination_count_query_arg: count, self.pagination_pk_query_arg: prev_page}))
        if next_page:
            links.update(dict(next={self.pagination_count_query_arg: count, self.pagination_pk_query_arg: next_page}))

        props = self.serialize_model(queryset, fields=self.list_fields)
        return props, dict(links=links)

    def update(self, lookup_keys, updates, *args, **kwargs):
        """
        Updates the model found with the lookup keys and returns
        the serialized model.

        :param dict lookup_keys:
        :param dict updates:
        :return:
        :rtype: dict
        :raises: NotFoundException
        """
        model = self.get_model(lookup_keys)
        for key, value in six.iteritems(updates):
            if key not in self.fields:
                continue
            setattr(model, key, value)
        model.save()
        return self.serialize_model(model)

    def delete(self, lookup_keys, *args, **kwargs):
        """
        Deletes the model found with lookup_keys

        :param dict okup_keys:
        :return: Empty dict
        """
        model = self.get_model(lookup_keys)
        model.delete()

    def get_model(self, lookup_keys):
        """
        Retrieves a model with the specified lookup keys

        :param dict lookup_keys: The fields and attributes that
            uniquely identify the model
        :return: The model if found
        :rtype: django.db.models.Model
        :raises: NotFoundException
        """
        try:
            return self.queryset.filter(**lookup_keys).get()
        except self.model.DoesNotExist as e:
            raise NotFoundException('No model of type {0} could be found using'
                                    ' lookup keys {1}'.format(self.model.__name__, lookup_keys))

    def serialize_model(self, model, fields=None):
        """
        :param model: The model or queryset that is being serialized.
        :type model: django.db.models.Model
        :param list fields: The list of fields to include in the serialization
        :return: The serialized model
        :rtype: dict
        """
        fields = fields or self.fields
        if isinstance(model, QuerySet):
            response = []
            for m in model:
                response.append(self.serialize_model(m, fields))
            return response

        response = {}
        for f in fields:
            response[f] = getattr(model, f)
        return sql_to_json_encoder(response)

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