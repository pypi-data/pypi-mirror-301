# -*- coding: utf-8 -*-
from lxml import etree as _etree
from urllib.parse import urlparse
from urllib.request import urlopen


def getDatabase(db):
    if not is_url(db.url):
        tree = _etree.parse(db.url)
        # can raise OSError (file not found, ...)
    else:
        with urlopen(db.url) as response:
            tree = _etree.fromstring(response.read().decode())
            # can raise urllib.error.HTTPError (HTTP Error 404: Not Found, ...)
    return tree


def is_url(path):
    schemes = ('http', 'https', )
    return urlparse(path).scheme in schemes


def createDatabase():
    xml_schema = 'http://www.w3.org/2001/XMLSchema-instance'
    hera_xsd = 'https://gitlab.huma-num.fr/datasphere/hera/schema/schema.xsd'
    qname = _etree.QName(xml_schema, 'schemaLocation')
    root = _etree.Element('hera', {qname: hera_xsd})
    properties = _etree.SubElement(root, 'properties')
    entities = _etree.SubElement(root, 'entities')
    items = _etree.SubElement(root, 'items')
    return root
