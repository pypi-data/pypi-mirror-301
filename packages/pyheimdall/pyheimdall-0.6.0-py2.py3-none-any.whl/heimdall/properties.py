# -*- coding: utf-8 -*-

"""
Provides CRUD operations to search for or
edit properties in a HERA element tree.

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""

from lxml import etree as _et
from .util import _get_node, _get_nodes, _get_root, _create_node, _create_nodes


def getProperty(tree, filter):
    """Retrieves a single property.

    This function works exactly like ``heimdall.getProperties``, but raises an
    ``IndexError`` if ``filter`` returns more than one result.

    :param tree: HERA elements tree
    :param filter: Filtering function
    :return: Item element
    :rtype: lxml.Element
    """
    return _get_node(tree, 'property', filter)


def getProperties(tree, filter=None):
    """Retrieves a collection of properties.

    :param tree: HERA element tree
    :param filter: (optional) Filtering function
    :return: List of Property elements
    :rtype: list

    This function can be used to retrieve all properties in a database: ::

      >>> import heimdall
      >>> ...  # create config
      >>> tree = heimdall.getDatabase(config)  # load HERA tree
      >>> items = heimdall.getProperties(tree)  # retrieve all properties

    To retrieve only *some* properties, you can use a filter.
    A filter is a function which takes only a property as a parameter, and
    returns either ``True`` (we want this property to be part of the list
    returned by ``getProperties``) or ``False`` (we don't want it). ::

      >>> import heimdall
      >>> ...  # create config, load HERA tree
      >>> def by_pid(property):  # create filtering function
      >>>     return property.get('id') == 'dc:name'
      >>> # retrieve only a specific property by its id
      >>> items = heimdall.getProperties(tree, by_pid)

    For simple filters, anonymous functions can of course be used: ::

      >>> import heimdall
      >>> ...  # create config, load HERA tree
      >>> # retrieve only a specific property by its id
      >>> heimdall.getItems(tree, lambda e: e.get('id') == 'dc:name')
    """
    return _get_nodes(tree, 'property', filter)


def createProperty(tree, id, **kwargs):
    r"""Creates a single property.

    :param tree: HERA element tree
    :param id: Property unique id
    :param \**kwargs: (optional) Keyword arguments, see below.
    :Keyword arguments:
        * **type** (``str``) -- (optional, default: ``text``) Property type
        * **name** (``str|dict``) -- (optional) Human-readable name
        * **type** (``str|dict``) -- (optional) Human-readable documentation
        * **uri** (``list``) -- (optional) URI list

    This function can be used to add a new property to a database.
    Elements created by ``createProperty`` will always be added to the
    ``<properties/>`` container element.

    In its simplest usage, ``createProperty`` simply creates
    a new ``<property id='xxx'/>`` element: ::

      >>> import heimdall
      >>> ...  # create config
      >>> tree = heimdall.getDatabase(config)  # load HERA tree
      >>> heimdall.createProperty(tree, id='xxx')  # create a new property
      >>> # the following child is now added to the properties list:
      >>> # <property id='xxx' />

    Each property identifier must be unique among all properties.
    Thus, calling ``createProperty`` with an ``id`` already in
    use by another property in the same database will fail.

    Additional supported parameters are ``type``, ``name``, ``description``,
    and ``uri``.
    Each of these parameters creates appropriate children for the property.
    Here is an example: ::

      >>> import heimdall
      >>> ...  # create config, load HERA tree
      >>> heimdall.createProperty(tree,
      >>>     id='dc:name', name='Name',
      >>>     uri=[
      >>>         'TODO dc',
      >>>         'TODO dtc'
      >>>     ])
      >>> # the following property is now added to the properties list:
      >>> # <property id='xxx'>
      >>> #     <type>text</type>
      >>> #     <name>Name</name>
      >>> #     <uri>TODO dc</uri>
      >>> #     <uri>TODO dtc</uri>
      >>> # </property>

    Please note that ``name`` and ``description`` can be localized, if they are
    of type ``dict`` instead of ``str`` (``dict`` keys are language codes).
    The following example shows property localization: ::

      >>> import heimdall
      >>> ...  # create HERA element tree
      >>>  heimdall.createProperty(tree, id='dc:name',
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
      >>> # <property id='dc:name'>
      >>> #     <type>text</type>
      >>> #     <name xml:lang='de'>Name</name>
      >>> #     <name xml:lang='en'>Name</name>
      >>> #     <name xml:lang='fr'>Nom</name>
      >>> #     <description xml:lang='en'>Human-readable name</description>
      >>> #     <description xml:lang='fr'>Nom usuel</description>
      >>> # </property>
    """
    container = tree.findall('.//properties')
    if container:
        container = container[0]
        nodes = container.getchildren()
    else:  # Create <properties/> node
        container = _et.SubElement(_get_root(tree), 'properties')
        nodes = []
    # Check property unique id (pid) does not exist
    if len([n for n in nodes if n.get('id') == id]) > 0:
        raise ValueError(f"Property id '{id}' already exists")
    # Create property
    node = _et.SubElement(container, 'property', id=id)
    param = kwargs.get('type', 'text')
    _create_node(node, 'type', param)
    param = kwargs.get('name', None)
    if param:
        _create_nodes(node, 'name', param)
    param = kwargs.get('description', None)
    if param:
        _create_nodes(node, 'description', param)
    param = kwargs.get('uri', [])
    if type(param) is not list:
        raise TypeError(f"'uri' expected:'list', got:'{type(param).__name__}'")
    for value in param:
        _create_node(node, 'uri', value)
    return node


def replaceProperty(property, **kwargs):
    """TODO: Not Implemented
    """
    raise ValueError("TODO: Not Implemented")


def updateProperty(property, **kwargs):
    """TODO: Not Implemented
    """
    raise ValueError("TODO: Not Implemented")


def deleteProperty(tree, filter):
    """Deletes a single property.

    This method doesn't delete any metadata, nor any attribute, referencing
    the deleted property.
    All elements referencing this property, if any, will become invalid.
    They should either be deleted or fixed accordingly.

    This function raises an ``IndexError`` if the filtering method ``filter``
    returns more than one result.
    If ``filter`` returns no result, this function does nothing,
    and does not raise any error.

    This function performs the property deletion "in place".
    In other words, parameter ``tree`` is directly modified,
    and this function returns nothing.

    :param tree: HERA elements tree
    :param filter: Filtering function

    Usage ::

      >>> import heimdall
      >>> ...  # create config, load HERA tree
      >>> # delete a property using its unique id
      >>> heimdall.deleteProperty(tree, lambda e: e.get('id') == '42')
    """
    node = _get_node(tree, 'property', filter)
    if node is not None:
        node.getparent().remove(node)


__copyright__ = "Copyright the pyHeimdall contributors."
__license__ = 'AGPL-3.0-or-later'
__all__ = [
    'getProperty', 'getProperties',
    'createProperty', 'deleteProperty',
    'replaceProperty', 'updateProperty',
    '__copyright__', '__license__',
    ]
