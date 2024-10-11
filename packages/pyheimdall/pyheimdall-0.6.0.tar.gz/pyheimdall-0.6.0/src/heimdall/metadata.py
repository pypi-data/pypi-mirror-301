# -*- coding: utf-8 -*-

"""
Provides CRUD operations to search for or
edit metadata in a HERA item.

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""

from .util import _create_nodes, _get_node


def getMetadata(item, pid=None, aid=None):
    """Retrieves metadata elements from an item.

    :param item: HERA item
    :param pid: HERA property identifier
    :return: Metadata as HERA elements
    :rtype: list

    This function works exactly like ``heimdall.getValues``, but returns
    HERA metadata elements instead of `str` values.

    Here is an example: ::

      >>> import heimdall
      >>> ...
      >>> item = getItem(...)
      >>> # consider we just got the following item:
      >>> # <item eid='person'>
      >>> #   <metadata pid='dc:name' xml:lang='en'>William</metadata>
      >>> #   <metadata pid='dc:name' xml:lang='fr'>Guillaume</metadata>
      >>> #   <metadata pid='pet'>Chirpy</metadata>
      >>> #   <metadata pid='pet'>Claws</metadata>
      >>> #   <metadata pid='pet'>Blackie</metadata>
      >>> # </item>
      >>> # then we'll have the following results
      >>> values = heimdall.getMetadata(item, 'dc:name')
      >>> # len(values) == 2
      >>> values = heimdall.getMetadata(item, 'pet')
      >>> # len(values) == 3
      >>> values = heimdall.getMetadata(item, 'meats')
      >>> # len(values) == 0

    If ``pid`` parameter is left undefined, ``getMetadata``
    simply returns all metadata elements of an item.
    In the above example, ``heimdall.getMetadata(item)`` would
    return a list of all (5) metadata elements of ``item``.
    """
    if aid:
        xpath = './/metadata[@aid="{aid}"]'.format(aid=aid)
        return item.findall(xpath)
    if pid:
        xpath = './/metadata[@pid="{pid}"]'.format(pid=pid)
        return item.findall(xpath)
    return item.findall('.//metadata')


def getValues(item, pid):
    """Retrieves metadata values from an item.

    :param item: HERA item
    :param pid: HERA property identifier
    :return: Metadata as ``str`` values
    :rtype: ``list``

    This function can be used to retrieve metadata values from an item.
    Here is an example: ::

      >>> import heimdall
      >>> ...
      >>> item = getItem(...)
      >>> # consider we just got the following item:
      >>> # <item eid='person'>
      >>> #   <metadata pid='dc:name' xml:lang='en'>William</metadata>
      >>> #   <metadata pid='dc:name' xml:lang='fr'>Guillaume</metadata>
      >>> #   <metadata pid='pet'>Chirpy</metadata>
      >>> #   <metadata pid='pet'>Claws</metadata>
      >>> #   <metadata pid='pet'>Blackie</metadata>
      >>> # </item>
      >>> # then we'll have the following results
      >>> values = heimdall.getValues(item, 'dc:name')
      >>> # values = ['William', 'Guillaume']
      >>> values = heimdall.getValues(item, 'pet')
      >>> # values = ['Chirpy', 'Claws', 'Blackie']
      >>> values = heimdall.getValues(item, 'meats')
      >>> # values = []
    """
    xpath = './/metadata[@pid="{pid}"]'.format(pid=pid)
    values = []
    for metadata in item.findall(xpath):
        if metadata.text is not None:
            values.append(metadata.text)
        else:  # <metadata ...></metadata>
            values.append('')
    return values


def getValue(item, pid):
    """Retrieves a single metadata value from an item.

    This function works exactly like ``heimdall.getValues``, but raises an
    ``IndexError`` if there is more than one metadata corresponding to ``pid``.

    :param item: HERA item
    :param pid: HERA property identifier
    :return: Metadata value
    :rtype: ``str``
    """
    values = getValues(item, pid)
    if len(values) == 0:
        return None
    if len(values) == 1:
        return values[0]
    raise IndexError("Too many metadata ({count})".format(count=len(values)))


def createMetadata(item, pid, aid, value):
    """Adds a single metadata to an item.

    :param item: HERA item
    :param pid: HERA property identifier
    :param value: Metadata value

    Metadata created by ``createMetadata`` will always be added
    to the item ``item``, with no consistency check.
    For example, ``createMetadata`` does not verify that ``pid`` is a valid
    property identifier in the database ``item`` comes from.
    Should ``item`` have a related entity, ``createMetadata`` does not check
    that the new metadata makes sense for the entity (*ie.* that the
    entity defines an attribute reusing the property ``pid``).

    The following example adds a new metadata to an existing item: ::

      >>> import heimdall
      >>> ...
      >>> item = getItem(...)
      >>> heimdall.createMetadata(item, 'dc:name', 'name_attr', 'Bill')

    Metada added to a ``item`` can be localized, if their value is given as
    a ``dict`` instead of a ``str`` (``dict`` keys are language codes).
    Here is an example: ::

      >>> import heimdall
      >>> ...
      >>> item = getItem(...)
      >>> heimdall.createMetadata(item, 'dc:name', 'name_attr', {
      >>>     'en_AU': 'Bill',
      >>>     'de_DE': 'Wilhelm',
      >>>     })
    """
    nodes = _create_nodes(item, 'metadata', value)
    for node in nodes:
        if pid:
            node.set('pid', pid)
        if aid:
            node.set('aid', aid)
    return nodes


def deleteMetadata(item, pid):
    """TODO
    """
    node = _get_node(item, 'metadata', lambda m: m.get('pid') == pid)
    if node is not None:
        node.getparent().remove(node)


__copyright__ = "Copyright the pyHeimdall contributors."
__license__ = 'AGPL-3.0-or-later'
__all__ = [
    'getMetadata', 'getValue', 'getValues',
    'createMetadata', 'deleteMetadata',
    '__copyright__', '__license__',
    ]
