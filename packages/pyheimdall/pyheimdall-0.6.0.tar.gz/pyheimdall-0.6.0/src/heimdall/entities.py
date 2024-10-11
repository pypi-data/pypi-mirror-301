# -*- coding: utf-8 -*-

"""
Provides CRUD operations to search for or
edit entities in a HERA element tree.

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""

from lxml import etree as _et
from .util import _get_node, _get_nodes, _get_root, _create_node, _create_nodes


def getEntity(tree, filter):
    """Retrieves a single entity.

    This function works exactly like ``heimdall.getEntities``, but raises an
    ``IndexError`` if ``filter`` returns more than one result.

    :param tree: HERA elements tree
    :param filter: Filtering function
    :return: Item element
    :rtype: lxml.Element
    """
    return _get_node(tree, 'entity', filter)


def getEntities(tree, filter=None):
    """Retrieves a collection of entities.

    :param tree: HERA elements tree
    :param filter: (optional) Filtering function
    :return: List of Entity elements
    :rtype: list

    This function can be used to retrieve all entities in a database: ::

      >>> import heimdall
      >>> ...  # create config
      >>> tree = heimdall.getDatabase(config)  # load HERA tree
      >>> entities = heimdall.getEntities(tree)  # retrieve all entities

    To retrieve only *some* entities, you can use a filter.
    A filter is a function which takes only an item as a parameter, and
    returns either ``True`` (we want this entity to be part of the list
    returned by ``getEntities``) or ``False`` (we don't want it). ::

      >>> import heimdall
      >>> ...  # create config, load HERA tree
      >>>
      >>> def by_attribute_property(attribute):  # attribute filter
      >>>     return attribute.get('pid', '101010')
      >>>
      >>> def by_property(entity):  # entity filter
      >>>     attribute = getAttribute(entity, by_attribute_property)
      >>>     return attribute is not None
      >>>
      >>> # retrieve only entities reusing a property of id '101010'
      >>> entities = heimdall.getEntities(tree, by_property)

    For simple filters, anonymous functions can of course be used: ::

      >>> import heimdall
      >>> ...  # create config, load HERA tree
      >>> # retrieve only entities of a specific id
      >>> heimdall.getEntities(tree, lambda e: e.getValue('id') == '42')
    """
    return _get_nodes(tree, 'entity', filter)


def createEntity(tree, id, **kwargs):
    r"""Creates a single entity.

    :param tree: HERA element tree
    :param id: Entity unique id
    :param \**kwargs: (optional) Keyword arguments, see below.
    :Keyword arguments:
        * **name** (``str|dict``) -- (optional) Human-readable name
        * **type** (``str|dict``) -- (optional) Human-readable documentation
        * **uri** (``list``) -- (optional) URI list

    This function can be used to add a new entity to a database.
    Entities created by ``createEntity`` will always be added to the
    ``<entities/>`` container element.

    In its simplest usage, ``createEntity`` simply creates
    a new ``<entity id='xxx'/>`` element: ::

      >>> import heimdall
      >>> ...
      >>> tree = heimdall.getDatabase(config)  # load HERA tree
      >>> heimdall.createEntity(tree, 'xxx')  # create a new entity
      >>> # the following child is now added to entities list:
      >>> # <entity pid='xxx' />

    Additional supported parameters are ``type``, ``name``, ``description``,
    and ``uri``.
    Each of these parameters creates appropriate children for the attribute.
    Here is an example: ::

      >>> import heimdall
      >>> ...  # load HERA tree
      >>> heimdall.createEntity(tree,
      >>>     id='person', name='Person',
      >>>     description="Real person or fictional character.",
      >>>     )
      >>> # the following entity is now added to entities list:
      >>> # <entity id='person'>
      >>> #     <name>Person</name>
      >>> #     <description>Person, real or not</description>
      >>> # </entity>

    Please note that ``name`` and ``description`` can be localized, if they are
    of type ``dict`` instead of ``str`` (``dict`` keys are language codes).
    The following example shows entity localization: ::

      >>> import heimdall
      >>> ...  # create HERA element tree
      >>>  heimdall.createAttribute(tree,
      >>>      id='person',
      >>>      name={
      >>>          'de': "Person",
      >>>          'en': "Person",
      >>>          'fr': "Personne",
      >>>      },
      >>>      description={
      >>>          'en': "Person, real or not",
      >>>          'fr': "Personne réelle ou non",
      >>>      })
      >>> # the following entity is now added to the entities list:
      >>> # <entity id='person'>
      >>> #     <name xml:lang='de'>Person</name>
      >>> #     <name xml:lang='en'>Person</name>
      >>> #     <name xml:lang='fr'>Persone</name>
      >>> #     <description xml:lang='en'>Person, real or not</description>
      >>> #     <description xml:lang='fr'>Personne réelle ou non</description>
      >>> # </entity>

    Once an entity is created, some attributes can be added to it.
    For example: ::

      >>> import heimdall
      >>> ...  # load HERA tree
      >>> e = heimdall.createEntity(tree, id='person', name='Person')
      >>> heimdall.createAttribute(e, pid='name', name="Name")
      >>> heimdall.createAttribute(e, pid='eyes', name="Eye color")
      >>> # the following entity is now added to entities list:
      >>> # <entity id='person'>
      >>> #     <name>Person</name>
      >>> #     <attribute pid='name'>
      >>> #         <name>Name</name>
      >>> #     </attribute>
      >>> #     <attribute pid='eyes'>
      >>> #         <name>Eye color</name>
      >>> #     </attribute>
      >>> # </entity>

    See `heimdall.createAttribute <#heimdall.createAttribute>`_
    for more info about adding attributes to an entity.
    """
    container = tree.findall('.//entities')
    if container:
        container = container[0]
        nodes = container.getchildren()
    else:  # Create <entities/> node
        container = _et.SubElement(_get_root(tree), 'entities')
        nodes = []
    # Check entity unique id (eid) does not exist
    if len([n for n in nodes if n.get('id') == id]) > 0:
        raise ValueError(f"Entity id '{id}' already exists")
    # Create entity
    node = _et.SubElement(container, 'entity', id=id)
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


def replaceEntity(entity, **kwargs):
    """TODO: Not Implemented
    """
    raise ValueError("TODO: Not Implemented")


def updateEntity(entity, **kwargs):
    """TODO: Not Implemented
    """
    raise ValueError("TODO: Not Implemented")


def deleteEntity(tree, filter):
    """Deletes a single entity.

    This method doesn't delete any item documented by the deleted entity.
    All items referencing this entity, if any, will become invalid.
    One can either delete these items afterwards, or change their ``eid``, or
    recreate a new entity and update these items accordingly.

    This function raises an ``IndexError`` if the filtering method ``filter``
    returns more than one result.
    If ``filter`` returns no result, this function does nothing,
    and does not raise any error.

    This function performs the entity deletion "in place".
    In other words, parameter ``tree`` is directly modified,
    and this function returns nothing.

    :param tree: HERA elements tree
    :param filter: Filtering function

    Usage ::

      >>> import heimdall
      >>> ...  # create config, load HERA tree
      >>> # delete a property using its unique id
      >>> heimdall.deleteEntity(tree, lambda e: e.get('id') == '42')
    """
    node = _get_node(tree, 'entity', filter)
    if node is not None:
        node.getparent().remove(node)


__copyright__ = "Copyright the pyHeimdall contributors."
__license__ = 'AGPL-3.0-or-later'
__all__ = [
    'getEntity', 'getEntities',
    'createEntity', 'deleteEntity',
    'replaceEntity', 'updateEntity',
    '__copyright__', '__license__',
    ]
