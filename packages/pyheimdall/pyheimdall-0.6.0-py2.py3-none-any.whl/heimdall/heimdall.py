#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Provides CRUD operations to search in or edit a HERA elements tree.

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""

from . import hera
from .properties import (
    getProperty, getProperties,
    createProperty, deleteProperty,
    replaceProperty, updateProperty,
    )
from .entities import (
    getEntity, getEntities,
    createEntity, deleteEntity,
    replaceEntity, updateEntity,
    )
from .attributes import (
    getAttribute, getAttributes,
    createAttribute, deleteAttribute,
    replaceAttribute, updateAttribute,
    )
from .items import (
    getItem, getItems,
    createItem, deleteItem,
    replaceItem, updateItem,
    )
from .metadata import (
    getMetadata, getValue, getValues,
    createMetadata, deleteMetadata,
    )
from . import json
from .sql import mysql
from lxml import etree
from .util import _get_node, _get_nodes, _get_root, _create_nodes

MODULES = {
    'xml:hera': hera,
    'json:hera': json,
    'sql:mysql': mysql,
    }


def getDatabase(db):
    """TODO
    """
    get = getattr(MODULES[db.format], 'getDatabase')
    tree = get(db)
    return tree


def createDatabase():
    """Create an empty database

    :return: HERA element tree
    :rtype: lxml.ElementTree
    """
    return hera.createDatabase()


class Config:
    def __init__(self, **entries):
        self.__dict__.update(entries)


__copyright__ = "Copyright the pyHeimdall contributors."
__license__ = 'AGPL-3.0-or-later'
__all__ = [
    'getDatabase',
    'createDatabase',

    'getProperty', 'getProperties',
    'createProperty', 'deleteProperty',
    'replaceProperty', 'updateProperty',

    'getEntity', 'getEntities',
    'createEntity', 'deleteEntity',
    'replaceEntity', 'updateEntity',
    'getAttribute', 'getAttributes',
    'createAttribute', 'deleteAttribute',
    'replaceAttribute', 'updateAttribute',

    'getItem', 'getItems',
    'createItem', 'deleteItem',
    'replaceItem', 'updateItem',
    'getMetadata', 'getValue', 'getValues',
    'createMetadata', 'deleteMetadata',

    'Config',  # TODO remove
    '__copyright__', '__license__',
    ]
