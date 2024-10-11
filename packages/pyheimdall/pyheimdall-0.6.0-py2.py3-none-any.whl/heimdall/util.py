# -*- coding: utf-8 -*-

"""
Provides utilities functions around HERA elements tree refactoring or cleanup.

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""

import heimdall
from lxml import etree


def _get_nodes(tree, tag, filter=None):
    nodes = tree.findall(f'.//{tag}')
    if filter:
        return [node for node in nodes if filter(node)]
    return nodes


def _get_node(tree, tag, filter=None):
    nodes = _get_nodes(tree, tag, filter)
    if len(nodes) == 0:
        return None
    if len(nodes) == 1:
        return nodes[0]
    raise IndexError(f"Too many {tag} elements ({len(nodes)})")


def _get_root(tree):
    return tree.xpath('//hera')[0]


def _create_nodes(parent, tag, text):
    nodes = list()
    if type(text) is str:
        node = _create_node(parent, tag, text)
        nodes.append(node)
    else:
        qname = etree.QName('http://www.w3.org/XML/1998/namespace', 'lang')
        for language_key, value in text.items():
            node = _create_node(parent, tag, value)
            node.set(qname, language_key)
            nodes.append(node)
    return nodes


def _create_node(parent, tag, text):
    node = etree.SubElement(parent, tag)
    node.text = text
    return node


def delete_unused_properties(tree, relational=True):
    """Delete unused properties from a HERA element tree.

    An unused property is not referenced by any attribute in the same tree
    (an attribute reuses a property via its ``pid``).
    Please note that if no attribute references a property, this property is
    deleted, even if one or more items in the tree reference this property.
    If an item metadata references an unused property,  the corresponding
    property is deleted anyway, as it has no use if the item's entity doesn't
    use the property via one of its attribute.

    | The previous paragraph description is valid for relational databases,
      but not for non-relational databases, where items directly use
      properties, and generally don't belong to any entities.
    | If your database is non-relational, a property isn't unused and
      shouldn't be deleted if one or more items reference it.
      To avoid this, set the ``relational`` parameter to ``False`` when using
      ``delete_unused_properties``.

    This function performs its modifications "in place".
    In other words, parameter ``tree`` is directly modified,
    and this function returns nothing.

    :param tree: HERA elements tree
    :param relational: (optional, default: ``True``) Set this parameter
       to ``False`` for non-relational specific behaviour (see description)

    Usage ::

      >>> from heimdall.util import delete_unused_properties
      >>> ...  # create config, load HERA tree
      >>> delete_unused_properties(tree)  # get rid of some clutter

    """

    # give ourselves a map of unused properties, initialized with all of them
    properties = {}
    for p in heimdall.getProperties(tree):
        properties[p.get('id')] = p
    # let's check which properties are really unused
    for e in heimdall.getEntities(tree):
        for a in heimdall.getAttributes(e):
            pid = a.get('pid')
            if pid in properties.keys():
                # this property is in use ; so we mustn't delete it
                properties.pop(pid)

    to_keep = []
    if not relational:
        for pid in properties.keys():
            for item in heimdall.getItems(tree):
                metadata = heimdall.getMetadata(item, pid)
                if len(metadata) > 0:
                    # item references pid, so property won't be deleted
                    to_keep.append(pid)

    # the map now only contains unused ones ; so, delete them
    # (if not relational, pid in `to_keep` ARE NOT deleted)
    for pid, p in properties.items():
        if pid not in to_keep:
            p.getparent().remove(p)
    # end of function, don't bother with properties.clear()


def merge_properties(tree, properties):
    """Merge duplicate properties.

    This function allows to merge this similar properties into an existing one.
    This makes the resulting database schema more readable, because
    similarities between items and entities are more apparent when
    properties are systematically reused.

    This function updates ``pid`` referenced by each item's metadata,
    as long as the ``pid`` referenced by each entity's attribute, if
    these ``pid`` correspond to keys of the ``properties`` map parameter.
    The updated value is the key's value in ``properties``.

    Please note that only each relevant entity's attribute ``pid`` is
    modified, so each one keeps its custom names, descriptions and whatnot.

    | As each key of ``properties`` has its own value, this method
      can be used to merge many "duplicate" properties into different
      "factorized" ones, all at once.
    | However, each value of ``properties`` must be the unique
      identifier of an existing property in ``tree``.

    After using ``merge_properties``, previous duplicate properties
    remain in place, albeit now unused.
    Thus, ``heimdall.util.delete_unused_properties`` can be called
    on the same ``tree`` to get rid of them.

    This function performs its modifications "in place".
    In other words, parameter ``tree`` is directly modified,
    and this function returns nothing.

    :param tree: HERA elements tree
    :param properties: Map containing old property identifiers as keys,
           and new property identifiers as values

    The example below shows how to reuse what is in fact the
    ``name`` property from Dublin Core, instead of entity-specific
    property names which are conceptually the same: ::

      >>> import heimdall
      >>> from heimdall.util import *
      >>> ...  # create config, load HERA tree
      >>> heimdall.createProperty(tree, 'dc:name', name="Name")
      >>> merge_properties(tree, {  # make reusage more apparent
      >>>     'book_title': 'dc:name',
      >>>     'author_name': 'dc:name',
      >>>     'character_name': 'dc:name',
      >>>     'thesaurus_keyword': 'dc:name',
      >>>     })
      >>> delete_unused_properties(tree)  # optional but nice
    """

    for item in heimdall.getItems(tree):
        for old, now in properties.items():
            metadata = heimdall.getMetadata(item, pid=old)
            for m in metadata:
                m.set('pid', now)

    for entity in heimdall.getEntities(tree):
        for old, now in properties.items():
            for attribute in heimdall.getAttributes(
                        entity, lambda a: a.get('pid') == old):
                heimdall.updateAttribute(attribute, pid=now)


class Relationship:
    def __init__(self, eid, source, target):
        self.eid = eid  # a Relationship is an Entity, it's its id
        self.source = source  # source attribute pid
        self.target = target  # target attribute pid


def refactor_relationship(tree, relationship, eid, euid, pid, cleanup=True):
    """TODO
    """
    # TODO only create property if not exists
    p = heimdall.createProperty(tree, id=pid)
    e = heimdall.getEntity(tree, lambda n: n.get('id') == eid)
    # TODO only create attribute if not exists
    a = heimdall.createAttribute(e, pid=pid)
    # iterate over all items belonging to the relationship entity
    items = heimdall.getItems(tree, lambda n: n.get('eid') == relationship.eid)
    for old in items:
        source = heimdall.getMetadata(old, relationship.source)[0].text
        target = heimdall.getMetadata(old, relationship.target)[0].text

        def is_source(item):
            is_of_entity = item.get('eid') == eid
            has_unique_id = False
            # Unique id shouldn't be a repeatable attribute,
            # but we know what real world looks like. Thus,
            # try to not break in this edge case, and let's
            # hope our caller knows what she does.
            for v in heimdall.getValues(item, euid):
                has_unique_id = has_unique_id or (v == source)
            return is_of_entity and has_unique_id

        # get the item which must contain the new repeatable metadata
        now = heimdall.getItem(tree, is_source)
        etree.SubElement(now, 'metadata', pid=pid).text = target
        if cleanup:
            # delete `old` relationship item, because it is
            # now represented by new metadata in item `now`
            old.getparent().remove(old)
    if cleanup:
        # delete the `relationship` entity, as there are no more items using it
        heimdall.deleteEntity(tree, lambda n: n.get('id') == relationship.eid)


def merge_l10n_attributes(
        tree, eid, languages,
        pid=None, aid=None,
        cleanup=True, update_items=True
        ):
    """Merge attributes that are in fact translations of one another.

    :param tree: HERA elements tree
    :param eid: Identifier of the HERA entity in ``tree``
            containing all attributes to merge
    :param languages: dict containing attribute ids (aid) as keys
            and language codes as values
            it's not the other way around in case you have more than one
            attribute for the same language
    :param pid: HERA attribute pid of merged attribute
    :param aid (optional, default ``{pid}_attr``): HERA attribute id
            (aid) other attributes must be merged into; if ``base_aid`` is not
            the id of an attribute already present in ``entity``, an attribute
            of this name and type ``text`` will be created
    :param cleanup: (optional, default: ``True``) True if attributes in
            ``languages`` should be removed from ``entity`` after they
            are merged; ``base_aid`` is of course never removed.

    Usage example: ::

      >>> import heimdall
      >>> tree == ...  # load HERA tree
      >>> # let's say `tree` contains this entity:
      >>> # <entity id='person'>
      >>> #     <attribute pid='name_de' id='person.name_de_attr'>
      >>> #         <name>Personenname</name>
      >>> #     <attribute>
      >>> #     <attribute pid='name_en' id='person.name_en_attr'>
      >>> #         <name>Name</name>
      >>> #         <description>Name of the person</description>
      >>> #     <attribute>
      >>> #     <attribute pid='name_fr' id='person.name_fr_attr'>
      >>> #         <name>Nom</name>
      >>> #         <description>Nom de la personne</description>
      >>> #     <attribute>
      >>> # </entity>
      >>> # MERGE "columns"/attributes that are translations of one another
      >>> # give ourselves a property for merging human-readable names
      >>> heimdall.createProperty(
      >>>     tree, 'dcmi:title', type='text',
      >>>     name={'en': "Title", 'fr': "Titre", },
      >>>     description={
      >>>         'en': "A name given to the resource.",
      >>>         'fr': "Nom de la ressource.",
      >>>         },
      >>>     uri=[
      >>>         'http://purl.org/dc/terms/title',
      >>>         'http://datacite.org/schema/kernel-4/title',
      >>>         ],
      >>>     )
      >>> # merge the_people names
      >>> e = heimdall.getEntity(tree, lambda n: n.get('id') == 'person')
      >>> merge_l10n_attributes(tree, e, {
      >>>     'person.name_de_attr': 'de',
      >>>     'person.name_en_attr': 'en',
      >>>     'person.name_fr_attr': 'fr',
      >>>     },
      >>>     aid='person.name',
      >>>     pid='dcmi:title')
      >>> # now entity person looks like that:
      >>> # <entity id='person'>
      >>> #     <attribute pid='dcmi:title' id='person.name'>
      >>> #         <name xml:lang='de'>Personenname</name>
      >>> #         <name xml:lang='en'>Name</name>
      >>> #         <name xml:lang='fr'>Nom</name>
      >>> #         <description xml:lang='en'>Name of the person</description>
      >>> #         <description xml:lang='fr'>Nom de la personne</description>
      >>> #     <attribute>
      >>> # </entity>
    """
    entity = heimdall.getEntity(tree, lambda n: n.get('id') == eid)
    if entity is None:
        raise ValueError(f"Entity '{eid}' doesn't exist")
    # Check all attr languages have same pid and type
    aids = list(k for k in languages.keys())
    first_aid = aids[0]
    first_a = heimdall.getAttribute(entity, lambda n: n.get('id') == first_aid)
    if first_a is None:
        raise ValueError(f"Unknown attribute identifier '{first_aid}'")
    base_pid = pid or first_a.get('pid')
    base_aid = aid or f'{base_pid}_attr'
    base_type = _get_node(first_a, 'type')
    if base_type is not None:
        base_type = base_type.text
    amin = 0
    # first pass: consistency checks
    for aid in aids[1:]:
        attr = heimdall.getAttribute(entity, lambda a: a.get('id') == aid)
        if attr is None:
            raise ValueError(f"Attribute '{aid}' doesn't exist in {eid}")
        atype = _get_node(attr, 'type')
        if atype is not None:
            atype = atype.text
        if atype != base_type:
            raise ValueError("Attributes don't all have the same type")
        amin = max(amin, int(attr.get('min')))
    # get or create the attribute that will merge all others of `languages`
    base_a = heimdall.getAttribute(entity, lambda n: n.get('id') == base_aid)
    if base_a is None:
        base_a = heimdall.createAttribute(
                entity, id=base_aid, pid=base_pid,
                min=amin, max=None,
                type=base_type,
                )
    # second pass: merge attributes, and ...
    # * ... if `cleanup` delete `language` attributes (except base_atr ofc)
    # * ... if `update_items`, update_items to use id = base_a.id / base_aid
    qname = etree.QName('http://www.w3.org/XML/1998/namespace', 'lang')
    items = []
    if update_items:
        items = heimdall.getItems(tree, lambda n: n.get('eid') == eid)
    for aid, language in languages.items():
        attr = heimdall.getAttribute(entity, lambda a: a.get('id') == aid)
        node = _get_node(attr, 'name')
        if node is not None:
            node.set(qname, language)
            base_a.append(node)
        node = _get_node(attr, 'description')
        if node is not None:
            node.set(qname, language)
            base_a.append(node)

        if cleanup and (aid != base_aid):
            attr.getparent().remove(attr)
        for item in items:
            for metadata in heimdall.getMetadata(item, aid=aid):
                metadata.set('aid', base_aid)
                metadata.set('pid', base_pid)
                metadata.set(qname, language)


__copyright__ = "Copyright the pyHeimdall contributors."
__license__ = 'AGPL-3.0-or-later'
