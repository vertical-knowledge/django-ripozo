from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

try:
    from django.db.models.fields.related import ForeignRelatedObjectsDescriptor, \
        RenameRelatedObjectDescriptorMethods, ReverseManyRelatedObjectsDescriptor, \
        ManyRelatedObjectsDescriptor, SingleRelatedObjectDescriptor
except ImportError:
    pass  # These are only for django versions < 1.8
from ripozo.resources.relationships import ListRelationship, Relationship
from ripozo.resources.restmixins import CRUDL
from ripozo.resources.constructor import ResourceMetaClass


from django_ripozo.manager import DjangoManager


def _get_pks(model):
    """
    Gets the primary key name as a tuple
    for a model
    """
    return model._meta.pk.name,


def _get_fields_for_model(model):
    """
    Gets all of the fields for the model
    """
    fields = []
    try:
        all_fields = model._meta.get_fields()
    except AttributeError:  # Django < 1.8
        return _get_fields_old_django(model)
    for field in all_fields:
        if not field.is_relation:
            fields.append(field.name)
            continue
        partial = field.name
        complete = '{0}.{1}'.format(partial, field.related_model._meta.pk.name)
        fields.append(complete)
    return fields


def _get_fields_old_django(model):
    """
    For django < 1.8
    """
    fields = [f.name for f in model._meta.fields]
    for name in dir(model):
        attr = getattr(model, name)
        if isinstance(attr, ForeignRelatedObjectsDescriptor):
            pk = attr.related.model._meta.pk.name
            fields.append('{0}.{1}'.format(name, pk))
    return fields


def _get_relationships(model):
    """
    Gets a tuple of appropriately constructed
    Relationship/ListRelationship models for the model
    """
    relationships = []
    try:
        all_fields = model._meta.get_fields()
    except AttributeError:  # Django < 1.8
        return _get_relationships_old_django(model)
    for field in all_fields:
        if not field.is_relation:
            continue
        rel_class = ListRelationship if field.one_to_many or field.many_to_many else Relationship
        rel = rel_class(field.name, relation=field.related_model.__name__)
        relationships.append(rel)
    return tuple(relationships)


def _get_relationships_old_django(model):
    """for django < 1.8"""
    relationships = []
    for name in dir(model):
        attr = getattr(model, name)
        if isinstance(attr, SingleRelatedObjectDescriptor):
            relation_name = attr.related.model.__name__
            relationships.append(Relationship(name, relation=relation_name))
        elif isinstance(type(attr), RenameRelatedObjectDescriptorMethods) or\
                isinstance(attr, ReverseManyRelatedObjectsDescriptor):
            relation_name = attr.field.rel.to.__name__
            if isinstance(attr, ReverseManyRelatedObjectsDescriptor):
                relationships.append(ListRelationship(name, relation=relation_name))
            else:
                relationships.append(Relationship(name, relation=relation_name))
        elif isinstance(attr, (ForeignRelatedObjectsDescriptor, ManyRelatedObjectsDescriptor)):
            relation_name = attr.related.model.__name__
            relationships.append(ListRelationship(name, relation=relation_name))
    return tuple(relationships)


def create_resource(model, resource_bases=(CRUDL,),
                    relationships=None, links=None, preprocessors=None,
                    postprocessors=None, fields=None, paginate_by=100,
                    auto_relationships=True, pks=None, create_fields=None,
                    update_fields=None, list_fields=None):
        """
        Creates a ResourceBase subclass by inspecting a SQLAlchemy
        Model. This is somewhat more restrictive than explicitly
        creating managers and resources.  However, if you only need
        any of the basic CRUD+L operations,

        :param sqlalchemy.Model model:  This is the model that
            will be inspected to create a Resource and Manager from.
            By default, all of it's fields will be exposed, although
            this can be overridden using the fields attribute.
        :param tuple resource_bases: A tuple of ResourceBase subclasses.
            Defaults to the restmixins.CRUDL class only.  However if you only
            wanted Update and Delete you could pass in
            ```(restmixins.Update,  restmixins.Delete)``` which
            would cause the resource to inherit from those two.
            Additionally, you could create your own mixins and pass them in
            as the resource_bases
        :param tuple relationships: extra relationships to pass
            into the ResourceBase constructor.  If auto_relationships
            is set to True, then they will be appended to these relationships.
        :param tuple links: Extra links to pass into the ResourceBase as
            the class _links attribute.  Defaults to an empty tuple.
        :param tuple preprocessors: Preprocessors for the resource class attribute.
        :param tuple postprocessors: Postprocessors for the resource class attribute.
        :param tuple fields: The fields to expose on the api.  Defaults to
            all of the fields on the model.
        :param bool auto_relationships: If True, then the SQLAlchemy Model
            will be inspected for relationships and they will be automatically
            appended to the relationships on the resource class attribute.
        :param list create_fields: A list of the fields that are valid when
            creating a resource.  By default this will be the fields without
            any primary keys included
        :param list update_fields: A list of the fields that are valid when
            updating a resource.  By default this will be the fields without
            any primary keys included
        :param list list_fields: A list of the fields that will be returned
            when the list endpoint is requested.  Defaults to the fields
            attribute.
        :return: A ResourceBase subclass and DjangoManager subclass
        :rtype: ResourceMetaClass
        """
        relationships = relationships or tuple()
        if auto_relationships:
            relationships += _get_relationships(model)
        links = links or tuple()
        preprocessors = preprocessors or tuple()
        postprocessors = postprocessors or tuple()
        pks = pks or _get_pks(model)
        fields = fields or _get_fields_for_model(model)
        list_fields = list_fields or fields

        create_fields = create_fields or [x for x in fields if x not in set(pks)]
        update_fields = update_fields or [x for x in fields if x not in set(pks)]

        manager_cls_attrs = dict(paginate_by=paginate_by, fields=fields, model=model,
                                 list_fields=list_fields, create_fields=create_fields,
                                 update_fields=update_fields)
        manager_class = type(str(model.__name__), (DjangoManager,), manager_cls_attrs)
        manager = manager_class()

        resource_cls_attrs = dict(preprocessors=preprocessors,
                                  postprocessors=postprocessors,
                                  _relationships=relationships, _links=links,
                                  pks=pks, manager=manager)
        res_class = ResourceMetaClass(str(model.__name__), resource_bases, resource_cls_attrs)
        return res_class
