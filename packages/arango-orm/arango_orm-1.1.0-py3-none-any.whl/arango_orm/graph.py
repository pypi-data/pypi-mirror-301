from inspect import isclass
from typing import Type

from .collections import Collection, Relation


class GraphConnection(object):
    def __init__(
        self,
        collections_from: Collection | list[Collection],
        relation,
        collections_to: Collection | list[Collection],
    ):
        "Create a graph connection object"

        self.collections_from = collections_from
        self.collections_to = collections_to

        if isclass(relation):
            assert issubclass(relation, Relation)

        else:
            relation._collections_from = collections_from
            relation._collections_to = collections_to

        self.relation = relation

    def __str__(self):
        ret = "<{}(collections_from={}, relation={}, collections_to={})>".format(
            self.__class__.__name__,
            str(self.collections_from),
            str(self.relation.__collection__),
            str(self.collections_to),
        )

        return ret

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        """
        Convert the GraphConnection relation to dict understandable by the underlying
        python-arango driver
        """

        cols_from = []
        cols_to = []

        if isinstance(self.collections_from, (list, tuple)):
            cols_from = self.collections_from
        else:
            cols_from = [
                self.collections_from,
            ]

        if isinstance(self.collections_to, (list, tuple)):
            cols_to = self.collections_to
        else:
            cols_to = [
                self.collections_to,
            ]

        from_col_names = [col.__collection__ for col in cols_from]
        to_col_names = [col.__collection__ for col in cols_to]

        return {
            "name": self.relation.__collection__,
            "from_collections": from_col_names,
            "to_collections": to_col_names,
        }


class Graph(object):
    __graph__ = None
    graph_connections = None

    def __init__(self, graph_name=None, graph_connections=None, connection=None):
        self.vertices = {}
        self.edges: dict[str, Relation] = {}
        self.edge_cols_from: dict[str, list[Collection]] = {}
        self.edge_cols_to: dict[str, list[Collection]] = {}
        self._db = connection
        self._graph = None
        self.inheritances = {}

        if graph_name is not None:
            self.__graph__ = graph_name

        if self._db is not None:
            self._graph = self._db.graph(self.__graph__)

        if graph_connections:
            self.graph_connections = graph_connections

        if self.graph_connections:
            for gc in self.graph_connections:
                froms = gc.collections_from
                if not isinstance(froms, (list, tuple)):
                    froms = [
                        froms,
                    ]

                tos = gc.collections_to
                if not isinstance(tos, (list, tuple)):
                    tos = [
                        tos,
                    ]

                # Note: self.vertices stores collection classes while self.edges stores
                # relation objects (not classes)
                for col in froms + tos:
                    if col.__collection__ not in self.vertices:
                        self.vertices[col.__collection__] = col

                if gc.relation.__collection__ not in self.edges:
                    self.edges[gc.relation.__collection__] = gc.relation
                    self.edge_cols_from[gc.relation.__collection__] = froms
                    self.edge_cols_to[gc.relation.__collection__] = tos

        # for col_name, col in [
        #     (col_name, col)
        #     for col_name, col in self.vertices.items()
        #     if len(col._inheritance_mapping) > 0
        # ]:
        #     subclasses = self._get_recursive_subclasses(col).union([col])

        #     if len(subclasses) > 1:
        #         _inheritances = {}
        #         for subclass in [
        #             subclass
        #             for subclass in subclasses
        #             if subclass.__name__ in col._inheritance_mapping
        #         ]:
        #             _inheritances[col._inheritance_mapping[subclass.__name__]] = subclass
        #         if len(_inheritances):
        #             self.inheritances[col_name] = _inheritances

    # def _get_recursive_subclasses(self, cls):
    #     return set(cls.__subclasses__()).union(
    #         [s for c in cls.__subclasses__() for s in self._get_recursive_subclasses(c)]
    #     )

    def relation(self, relation_from, relation, relation_to):
        """
        Return relation (edge) object from given collection (relation_from and
        relation_to) and edge/relation (relation) objects
        """

        # relation._from = relation_from.__collection__ + '/' + relation_from._key
        # relation._to = relation_to.__collection__ + '/' + relation_to._key
        relation.from_ = relation_from.id_
        relation.to_ = relation_to.id_

        return relation

    def _inheritance_mapping_inspector(self, collection_class: Collection, doc_dict: dict):
        field = collection_class._inheritance_field
        mapping = self.inheritances[collection_class.__collection__]

        if doc_dict[field] not in mapping or not issubclass(mapping[doc_dict[field]], Collection):
            return False

        return mapping[doc_dict[field]]

    def inheritance_mapping_resolver(self, col_name: str, doc_dict) -> Type[Collection]:
        """
        Custom method to resolve inheritance mapping.

        It allows the user to resolve the class of the current object based on any condition (discriminator field a/o
        inference).

        :param col_name: The collection name retrieved from the object _id property
        :param doc_dict: The object as dict
        :return Type[Collection]
        """
        return self.vertices[col_name]

    def _doc_from_dict(self, doc_dict):
        "Given a result dictionary, creates and returns a document object"

        col_name = doc_dict["_id"].split("/")[0]
        CollectionClass = self.vertices[col_name]

        if CollectionClass.__collection__ in self.inheritances:
            found_class = self._inheritance_mapping_inspector(CollectionClass, doc_dict)
            if issubclass(found_class, Collection):
                CollectionClass = found_class

        elif callable(self.inheritance_mapping_resolver):
            resolved_class = self.inheritance_mapping_resolver(col_name, doc_dict)
            if issubclass(resolved_class, Collection):
                CollectionClass = resolved_class

        # remove empty values
        keys_to_del = []
        for k, v in doc_dict.items():
            if doc_dict[k] is None:
                keys_to_del.append(k)

        if keys_to_del:
            for k in keys_to_del:
                del doc_dict[k]

        return CollectionClass(**doc_dict)

    def _objectify_results(self, results, doc_obj=None):
        """
        Make traversal results object oriented by adding all links to the first
        object's _relations attribute. If doc_obj is not provided, the first
        vertex of the first path is used.
        """

        # Create objects from vertices dicts
        documents = {}
        if doc_obj:
            documents[doc_obj.id_] = doc_obj

        relations_added = {}

        for p_dict in results:
            for v_dict in p_dict["vertices"]:
                if doc_obj is None:
                    # Get the first vertex of the first result, it's the parent object
                    doc_obj = self._doc_from_dict(v_dict)
                    documents[doc_obj.id_] = doc_obj

                if v_dict["_id"] in documents:
                    continue

                # Get ORM class for the collection
                documents[v_dict["_id"]] = self._doc_from_dict(v_dict)

            # Process each path as a unit
            # First edge's _from always points to our parent document
            parent_id = doc_obj.id_

            for e_dict in p_dict["edges"]:
                col_name = e_dict["_id"].split("/")[0]
                rel_identifier = parent_id + "->" + e_dict["_id"]

                if rel_identifier in relations_added:
                    rel = relations_added[rel_identifier]

                else:
                    RelationClass = self.edges[col_name]

                    if not isclass(self.edges[col_name]):
                        RelationClass = RelationClass.__class__

                    rel = RelationClass(**e_dict)
                    rel._object_from = documents[rel.from_]
                    rel._object_to = documents[rel.to_]

                    parent_object = None
                    if rel.from_ == parent_id:
                        parent_object = documents[rel.from_]
                        rel._next = rel._object_to

                    elif rel.to_ == parent_id:
                        parent_object = documents[rel.to_]
                        rel._next = rel._object_from

                    assert parent_object is not None

                    if not hasattr(parent_object, "_relations"):
                        setattr(parent_object, "_relations", {})

                    if col_name not in parent_object._relations:
                        parent_object._relations[col_name] = []

                    if rel not in parent_object._relations[col_name]:
                        parent_object._relations[col_name].append(rel)

                    if rel.id_ not in relations_added:
                        relations_added[rel_identifier] = rel

                # Set parent ID
                if rel.from_ == parent_id:
                    parent_id = rel.to_

                elif rel.to_ == parent_id:
                    parent_id = rel.from_

        return doc_obj

    def expand(self, doc_obj, direction="any", depth=1, only=None, condition:str = None):
        """
        Graph traversal.

        Expand all links of given direction (outbound, inbound, any) upto given
        length for the given document object and update the object with the
        found relations.

        :param only: If given should be a string, Collection class or list of
        strings or collection classes containing target collection names of
        documents (vertices) that should be fetched.
        Any vertices found in traversal that don't belong to the specified
        collection names given in this parameter will be ignored.

        :param condition: String containing conditions in JS format. If `only` is provided
        then these conditions are merged with only using logical AND. Within the condition
        3 objects (config, vertex, path) are available for use within the traversal context.
        """
        assert direction in ("any", "inbound", "outbound")

        graph = self._db.graph(self.__graph__)
        doc_id = doc_obj.id_
        doc_obj._relations = {}  # clear any previous relations
        filter_func = None
        c_str = ""

        aql = f"FOR vertex, edge, path IN 1..{depth} {direction} '{doc_id}' GRAPH {self.__graph__}\n"

        if only:
            if not isinstance(only, (list, tuple)):
                only = [
                    only,
                ]

            for c in only:
                if not isinstance(c, str) and hasattr(c, "__collection__"):
                    c = c.__collection__

                c_str += "vertex._id LIKE '" + c + "/%' ||"

            if c_str:
                c_str = c_str[:-3]

        if condition:
            if c_str:
                c_str = c_str + ' AND ' + condition
            else:
                c_str = condition

        if c_str:
            aql += "FILTER " + c_str + "\n"


        aql += "RETURN path"

        # print(aql)

        new_doc = self.aql(aql)
        if new_doc:
            doc_obj._relations = new_doc._relations

        # results = graph.traverse(
        #     start_vertex=doc_id,
        #     direction=direction,
        #     vertex_uniqueness="path",
        #     min_depth=1,
        #     max_depth=depth,
        #     filter_func=filter_func,
        # )


        # self._objectify_results(results["paths"], doc_obj)

    def aql(self, query, **kwargs):
        """Run AQL graph traversal query."""
        results = self._db.aql.execute(query, **kwargs)

        doc_obj = self._objectify_results(results)

        return doc_obj

    def delete_tree(self, doc_obj):
        """
        Remove node and all nodes linked to it based on traversal criteria.

        Only nodes present in doc_obj._relations dict are removed.
        """
        objs_to_delete = [doc_obj]

        def get_linked_objects(obj):
            ret = []
            for _, e_objs in getattr(obj, "_relations", {}).items():
                for e_obj in e_objs:
                    ret.append(e_obj)
                    v_obj = e_obj._next
                    ret.append(v_obj)

                    if hasattr(v_obj, "_relations"):
                        _ = get_linked_objects(v_obj)

            return ret

        if hasattr(doc_obj, "_relations"):
            objs_to_delete.extend(get_linked_objects(doc_obj))

        for obj in reversed(objs_to_delete):
            self._db.delete(obj)

        doc_obj._relations = {}
