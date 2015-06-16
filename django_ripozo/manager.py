from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.db import models
from django.db.models.query import QuerySet
from django.db.models.manager import Manager
from django.db.models.fields.related import ForeignObjectRel, ForeignKey

from ripozo.exceptions import NotFoundException
from ripozo.managers.base import BaseManager
from ripozo.resources.fields.common import BaseField, StringField, \
    BooleanField, FloatField, DateTimeField, IntegerField
from ripozo.utilities import make_json_safe

import logging
import six

logger = logging.getLogger(__name__)


class DjangoManager(BaseManager):
    """
    :param model: The django database model that this manager
        is responsible for handling
    :type model: django.db.models.Model
    """
    pagination_pk_query_arg = 'page'

    @property
    def queryset(self):
        """
        By default returns the self.model.objects
        If you wish to restrict the records available
        override this.
        """
        return self.model.objects

    @staticmethod
    def _get_field_python_type(model, name):
        """
        Gets the python type for the attribute on the model
        with the name provided.

        :param Model model: The Django model class.
        :param unicode name: The column name on the model
            that you are attempting to get the python type.
        :return: The python type of the column
        :rtype: type
        """
        parts = name.split('.')
        for m in parts:
            if isinstance(model, ForeignKey):
                model = model.related_model
            if isinstance(model, ForeignObjectRel):
                model = model.model
            model = model._meta.get_field_by_name(m)[0]
        return model

    @classmethod
    def get_field_type(cls, name):
        """
        :param unicode name: The name of the field to get the
            ripozo field type from.
        :return: The ripozo field type that most closely
            matches the database type.
        :rtype: ripozo.viewsets.fields.base.BaseField
        """
        column = cls._get_field_python_type(cls.model, name)
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
        logger.info('Creating model {0} with values {1}'.format(self.model.__name__, values))
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
        logger.info('Retrieving an individual model {0} with lookup '
                    'keys {1}'.format(self.model.__name__, lookup_keys))
        model = self.get_model(lookup_keys)
        return self.serialize_model(model)

    def retrieve_list(self, filters, *args, **kwargs):
        """
        Retrieves a list of records.

        :param dict filters:
        :return:
        :rtype:
        """
        logger.info('Retrieving list of {0} with filters '
                    '{1}'.format(self.model.__name__, filters))
        count = filters.pop(self.pagination_count_query_arg, self.paginate_by)
        page = filters.pop(self.pagination_pk_query_arg, 1)
        page -= 1  # Pages shouldn't be zero-indexed

        offset = page * count
        total = self.queryset.filter(**filters).count()
        queryset = self.queryset.filter(**filters)[offset:offset + count]

        prev_page = None
        next_page = None

        # Weird additions due to how it's actually exposed.
        if total > offset + count:
            next_page = page + 2
        if page > 0:
            prev_page = page
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
        logger.info('Updating model {0} with lookup keys {1}: values = '
                    '{2}'.format(self.model.__name__, lookup_keys, updates))
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
        logger.info('Attempting to delete model {0} with lookup keys '
                    '{1}'.format(self.model.__name__, lookup_keys))
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
        except self.model.DoesNotExist:
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
        field_dict = self.dot_field_list_to_dict(fields=fields)
        response = self._serialize_model_helper(model, field_dict=field_dict)
        return make_json_safe(response)

    def _serialize_model_helper(self, model, field_dict=None):
        # TODO docs
        if model is None:
            return None

        if isinstance(model, Manager):
            model = model.all()

        if isinstance(model, (QuerySet,)):
            model_list = []
            for m in model:
                model_list.append(self._serialize_model_helper(m, field_dict=field_dict))
            return model_list

        model_dict = {}
        for name, sub in six.iteritems(field_dict):
            value = getattr(model, name)
            if sub:
                value = self._serialize_model_helper(value, field_dict=sub)
            model_dict[name] = value
        return model_dict

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