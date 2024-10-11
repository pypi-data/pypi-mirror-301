# -*- coding: utf-8 -*-

"""
Provides CRUD operations to search for or
edit attributes in a HERA entity.

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""

from lxml import etree as _et
from .util import _get_node, _get_nodes, _get_root, _create_node, _create_nodes


def getAttribute(entity, filter):
    """Retrieves a single attribute from an entity.

    This function works exactly like ``heimdall.getAttributes``, but raises an
    ``IndexError`` if ``filter`` returns more than one result.

    :param tree: HERA elements tree
    :param filter: Filtering function
    :return: Attribute element
    :rtype: lxml.Element
    """
    return _get_node(entity, 'attribute', filter)


def getAttributes(entity, filter=None):
    """TODO
    """
    return _get_nodes(entity, 'attribute', filter)


def createAttribute(entity, pid, **kwargs):
    r"""Adds a single attribute to an entity.

    :param entity: HERA entity
    :param pid: Linked property ID
    :param \**kwargs: (optional) Keyword arguments, see below.
    :Keyword arguments:
        * **id** (``str``) -- (optional) Attribute id
        * **min** (``int``) -- (optional, default: ``0``)
          Minimum occurences in an item: ``1`` or more means it is mandatory
        * **max** (``int``) -- (optional)
          Maximum occurences in an item: ``1`` means it is not repeatable, more
          (or no value) means it is; ``0`` or ``<min`` is undefined behaviour
        * **type** (``str``) -- (optional) Type override;
          no value means the linked property ``type`` will be used
        * **name** (``str|dict``) -- (optional) Name override;
          no value means the linked property ``name`` will be used
        * **description** (``str|dict``) -- (optional) Description override;
          no value means the linked property ``description`` will be used
        * **uri** (``list``) -- (optional) URI list override;
          no value means the linked property ``uri`` will be used,
          any value adds to the property ``uri``

    This function can be used to add a new attribute to an existing entity.
    Attributes created by ``createAttribute`` will always be added to the
    entity ``entity``, with no consistency check.
    For example, ``createAttribute`` does not verify that ``pid`` is a valid
    property identifier in the database ``entity`` comes from.

    In its simplest usage, ``createAttribute`` simply creates
    a new ``<attribute pid='xxx'/>`` element: ::

      >>> import heimdall
      >>> ...
      >>> entity = heimdall.getEntity(...)
      >>> heimdall.createAttribute(entity, pid='xxx')  # create a new attribute
      >>> # the following child is now added to entity attributes list:
      >>> # <attribute pid='xxx' />

    Additional supported parameters are ``type``, ``name``, ``description``,
    and ``uri``.
    Each of these parameters creates appropriate children for the attribute.
    Here is an example: ::

      >>> import heimdall
      >>> ...
      >>> heimdall.createAttribute(entity,
      >>>     pid='dc:name', name='Name',
      >>>     uri=[
      >>>         'TODO dc',
      >>>         'TODO dtc'
      >>>     ])
      >>> # the following attribute is now added to the entity:
      >>> # <attribute pid='dc:name'>
      >>> #     <type>text</type>
      >>> #     <name>Name</name>
      >>> #     <uri>TODO dc</uri>
      >>> #     <uri>TODO dtc</uri>
      >>> # </attribute>

    Please note that ``name`` and ``description`` can be localized, if they are
    of type ``dict`` instead of ``str`` (``dict`` keys are language codes).
    The following example shows attribute localization: ::

      >>> import heimdall
      >>> ...  # create HERA element tree
      >>>  heimdall.createAttribute(entity,
      >>>      pid='dc:name',
      >>>      max='1',
      >>>      name={
      >>>          'de': "Name",
      >>>          'en': "Name",
      >>>          'fr': "Nom",
      >>>      },
      >>>      description={
      >>>          'en': "Human-readable name",
      >>>          'fr': "Nom usuel",
      >>>      })
      >>> # the following item is now added to the properties list:
      >>> # <attribute pid='dc:name' min='0' max='1'>
      >>> #     <type>text</type>
      >>> #     <name xml:lang='de'>Name</name>
      >>> #     <name xml:lang='en'>Name</name>
      >>> #     <name xml:lang='fr'>Nom</name>
      >>> #     <description xml:lang='en'>Human-readable name</description>
      >>> #     <description xml:lang='fr'>Nom usuel</description>
      >>> # </attribute>
    """
    # TODO check pid is not already in use in the entity
    node = _et.SubElement(entity, 'attribute', pid=pid)

    param = kwargs.get('id', None)
    if param is not None:
        # Check attribute unique id (aid) does not exist
        if getAttribute(entity, lambda a: a.get('id') == param) is not None:
            raise ValueError(f"Attribute id '{param}' already exists")
        node.set('id', str(param))
    param = kwargs.get('min', 0)
    node.set('min', str(int(param)))
    param = kwargs.get('max', None)
    if param is not None:
        node.set('max', str(int(param)))

    param = kwargs.get('type', None)
    if param is not None:
        _create_node(node, 'type', param)
    param = kwargs.get('name', None)
    if param is not None:
        _create_nodes(node, 'name', param)
    param = kwargs.get('description', None)
    if param is not None:
        _create_nodes(node, 'description', param)
    param = kwargs.get('uri', [])
    if type(param) is not list:
        raise TypeError(f"'uri' expected:'list', got:'{type(param).__name__}'")
    for value in param:
        _create_node(node, 'uri', value)
    return node


def replaceAttribute(attribute, **kwargs):
    """TODO: Not Implemented
    """
    raise ValueError("TODO: Not Implemented")


def updateAttribute(attribute, **kwargs):
    """TODO
    """

    def _maybe_set_value(key):
        try:
            value = kwargs[key]
            if value is not None:
                attribute.set(key, str(value))
            else:  # remove value
                attribute.attrib.pop(key)
        except KeyError:
            pass  # nothing to change

    _maybe_set_value('id')
    _maybe_set_value('pid')
    _maybe_set_value('min')
    _maybe_set_value('max')

    def _maybe_update_child(key):
        try:
            value = kwargs[key]
            children = _get_nodes(attribute, key)
            for child in children:
                if value is not None:
                    child.text = str(value)
                else:  # remove child node
                    child.getparent().remove(child)
        except KeyError:
            pass  # nothing to change

    _maybe_update_child('type')
    _maybe_update_child('name')
    _maybe_update_child('description')
    _maybe_update_child('uri')


def deleteAttribute(entity, filter):
    """Deletes a single Attribute from an entity.

    This method doesn't delete any metadata referencing the ``pid`` of the
    deleted attribute.

    This function raises an ``IndexError`` if the filtering method ``filter``
    returns more than one result.
    If ``filter`` returns no result, this function does nothing,
    and does not raise any error.

    This function performs the attribute deletion "in place".
    In other words, parameter ``tree`` is directly modified,
    and this function returns nothing.

    :param tree: HERA elements tree
    :param filter: Filtering function

    Usage ::

      >>> import heimdall
      >>> ...  # create config, load HERA tree
      >>> # delete an attribute of a specific entity
      >>> e = heimdall.getEntity(tree, lambda e : e.get('id') == 'person')
      >>> heimdall.deleteAttribute(e, lambda a: a.get('pid') == 'religion')
    """
    node = _get_node(entity, 'attribute', filter)
    if node is not None:
        node.getparent().remove(node)


__copyright__ = "Copyright the pyHeimdall contributors."
__license__ = 'AGPL-3.0-or-later'
__all__ = [
    'getAttribute', 'getAttributes',
    'createAttribute', 'deleteAttribute',
    'replaceAttribute', 'updateAttribute',
    '__copyright__', '__license__',
    ]
