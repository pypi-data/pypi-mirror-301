# -*- coding: utf-8 -*-
import heimdall
from urllib.parse import urlparse
from lxml import etree
available = True
try:
    from mysql.connector import connect
except ModuleNotFoundError:
    available = False


def getDatabase(db):
    if not available:
        raise ModuleNotFoundError("Module 'mysql-connector-python' required.")
    connection = _connect(db)
    with connection.cursor() as cursor:
        hera = _create_tree(db.entities, cursor)
    connection.close()
    return hera


def _connect(db):
    url = urlparse(db.url)
    # due to urlparse, url.path is something like '/dbname'
    # but mysql.connector.connect wants database = 'dbname'
    connection = connect(database=url.path.split('/')[1],
                         user=url.username, password=url.password,
                         host=url.hostname, port=url.port)
    # TBD: can connection.is_connected() be False here?
    return connection


def _create_tree(tables, cursor):
    root = heimdall.createDatabase()
    properties = root.xpath('//properties')[0]
    entities = root.xpath('//entities')[0]
    items = root.xpath('//items')[0]
    for table in tables:
        # create entity for this table
        entity, aid_vs_property = _create_entity(table, cursor)
        entities.append(entity)
        # create properties for this entity
        for p in aid_vs_property.values():
            properties.append(p)
        # create items for this entity
        eid = entity.get('id')
        result = cursor.execute(f'SELECT * FROM {table}')
        for row in cursor.fetchall():
            items.append(_create_item(eid, row, aid_vs_property))
    return root


def _create_item(eid, row, aid_vs_property):
    item = etree.Element('item', {'eid': eid, })
    for index, (aid, p) in enumerate(aid_vs_property.items()):
        value = row[index]
        if value is None:
            continue
        item.append(_create_metadata(value, aid=aid, pid=p.get('id')))
    return item


def _create_metadata(value, pid=None, aid=None):
    metadata = etree.Element('metadata')
    if aid is not None:
        metadata.set('aid', aid)
    if pid is not None:
        metadata.set('pid', pid)
    metadata.text = str(value)
    return metadata


def _create_entity(table, cursor):
    cursor.execute(f'SHOW CREATE TABLE {table}')
    create_table_query = cursor.fetchall()[0][1]
    entity = etree.Element('entity', {'id': table, })
    etree.SubElement(entity, 'name').text = table
    comment = _get_table_comment(create_table_query)
    if comment is not None:
        etree.SubElement(entity, 'description').text = comment

    aid_vs_property = dict()
    cursor.execute(f'SHOW FULL COLUMNS FROM {table}')
    for row in cursor.fetchall():
        a = _create_attribute(table, row)
        entity.append(a)
        aid_vs_property[a.get('id')] = _create_property(table, row)
    return entity, aid_vs_property


def _get_table_comment(create_table_query):
    import re
    pattern = re.compile(r"COMMENT='(?P<res>[\w\s]*)'")
    m = pattern.search(create_table_query)
    return m.group('res') if m is not None else None


def _create_attribute(table, row):
    # @see https://dev.mysql.com/doc/refman/8.4/en/show-columns.html
    name = row[0]
    sqltype = row[1]
    collation = row[2]
    nullability = row[3]  # YES|NO
    indexed = row[4]  # PRI|UNI|MUL
    default_value = row[5]
    extra = row[6]
    privileges = row[7]
    comment = row[8]
    root = etree.Element('attribute', {
        'id': f'{table}.{name}_attr', 'pid': f'{table}.{name}',
        'min': str(0) if nullability == 'YES' else str(1),
        'max': str(1),  # TODO hera allows repeatability, sql does not (as is)
        })
    etree.SubElement(root, 'type').text = _type_sql2hera(sqltype)
    etree.SubElement(root, 'name').text = name
    if comment:
        etree.SubElement(root, 'description').text = comment
    return root


def _create_property(table, row):
    # @see https://dev.mysql.com/doc/refman/8.4/en/show-columns.html
    name = row[0]
    sqltype = row[1]
    comment = row[8]
    root = etree.Element('property', id=f'{table}.{name}')
    etree.SubElement(root, 'type').text = _type_sql2hera(sqltype)
    etree.SubElement(root, 'name').text = name
    if comment is not None:
        etree.SubElement(root, 'description').text = comment
    return root


def _type_sql2hera(sqltype):
    if (sqltype == 'date' or
            sqltype == 'datetime' or
            sqltype == 'timestamp'):
        return 'datetime'
    if (sqltype.startswith('varchar') or
            sqltype.startswith('char') or
            sqltype.startswith('tinytext')):
        return 'text'
    if (sqltype.startswith('int') or
            sqltype.startswith('tinyint')):
        return 'number'
    raise ValueError(f"Unknown type '{sqltype}'")
