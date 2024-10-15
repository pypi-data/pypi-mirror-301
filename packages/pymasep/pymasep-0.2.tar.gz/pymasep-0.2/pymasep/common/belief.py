from typing import Optional, Tuple, List
from xml.etree.ElementTree import Element, SubElement
from hashlib import md5

import networkx as nx
from networkx_query import search_direct_relationships, search_nodes, search_relationships, PathCriteria

from pymasep.common import BaseObject


class Belief(BaseObject):
    """
    The Belief of an agent is all the agent knows about the world and that could have an influence on their actions.
    Here, the concept of Belief is more inspired by the BDI agent architecture than by the belief of a DEC-POMDP.

    Beliefs are based on Conceptual Graphs :cite:`sowa_conceptual_1984` :cite:`chein_graph-based_2008`. This version is limited to a
    simpler version of conceptual graphs. It has been tested with belief of three nodes (concept-relation-concept)
    See test_belief.py for more details.
    """

    def __init__(self, environment,
                 name: str = None,
                 template=None,
                 xml_node: Optional[Element] = None,
                 parent=None):
        """
        NOTE: Contrary to other BaseObjects,
        src_copy is not used for Belief since Belief instances are never copied
        but stay as the same reference in the current state

        :param environment: An Environment instance
        :param name: name of the Belief.
        :param xml_node: XML used to create the object.
        :param template: Template of the Belief. Needed if no xml_node or src_copy
        :param parent: parent object (see objects hierarchy)
        """
        super().__init__(environment=environment, name=name, template=template, xml_node=xml_node, parent=parent)

        self.beliefs = nx.Graph()
        """ beliefs data as a conceptual graph """

    @BaseObject.state.getter
    def state(self) -> str:
        """
        State of the Belief. Always 'run'

        :return: The state of Belief
        """
        return 'run'

    def id_str(self) -> str:
        """
        Create an str unique ID of the Belief

        :return: the string unique ID
        """
        lines = nx.generate_graphml(self.beliefs, encoding='utf-8')
        graph_str = ''.join(lines)
        return super().id_str() + md5(graph_str.encode()).hexdigest()

    def node_id(self,
                g: nx.Graph,
                c: Optional[Tuple[str] | Tuple[str, str]] = None,
                cr: Optional[List[Tuple[str, str]]] = None) -> int:
        """
        Get or create the node id of a node in the Belief.

        :param g: The graph to create the node id for
        :param c: the tuple of attribute of the node id to search if the node already exists
        :param cr: if c is a relation, this parameter represents the concepts linked to the relation
        """
        result = g.number_of_nodes() + 1
        if c is not None:
            l = None
            if len(c) == 2:  # Concept
                l = list(search_nodes(g, {'and': [{'eq': [('c',), c[0]]}, {'eq': [('v',), c[1]]}]}))
            else:
                if len(c) == 1:  # Relation
                    l1 = list(search_direct_relationships(g,
                                                          source={'and': [{'eq': [('c',), cr[0][0]]},
                                                                          {'eq': [('v',), cr[0][1]]}]},
                                                          target={'eq': [('c',), c[0]]}))
                    l2 = list(search_direct_relationships(g,
                                                          source={'eq': [('c',), c[0]]},
                                                          target={'and': [{'eq': [('c',), cr[1][0]]},
                                                                          {'eq': [('v',), cr[1][1]]}]}))
                    # print(c, cr, l1, l2)
                    if len(l1) == 1: l = [l1[0][1]]
                    if len(l2) == 1: l = [l2[0][0]]
            if l is not None and len(l) == 1:
                result = l[0]
        return result

    def add(self, c1: Tuple[str, str], r: Tuple[str], c2: Tuple[str, str]) -> None:
        """
        Adding two concepts linked with one relation into the belief

        :param c1: First concept as a tuple (concept, instance of the concept)
        :param r: relation between concepts.
        :param c2: Second concept as a tuple (concept, instance of the concept)
        """
        n1 = self.node_id(self.beliefs, c1)
        self.beliefs.add_node(n1, c=c1[0], v=c1[1])
        n2 = self.node_id(self.beliefs, r, cr=[c1, c2])
        self.beliefs.add_node(n2, c=r[0])
        n3 = self.node_id(self.beliefs, c2)
        self.beliefs.add_node(n3, c=c2[0], v=c2[1])
        self.beliefs.add_edge(n1, n2)
        self.beliefs.add_edge(n2, n3)

    def _create_request(self, c1: Tuple[str, str], r, c2):
        result = nx.Graph()
        n1 = self.node_id(result)
        result.add_node(n1, c=c1[0], v=c1[1], type='c')
        n2 = self.node_id(result)
        result.add_node(n2, c=r, type='r')
        n3 = self.node_id(result)
        result.add_node(n3, c=c2[0], v=c2[1], type='c')
        result.add_edge(n1, n2)
        result.add_edge(n2, n3)
        return result

    def query(self, query: nx.Graph) -> nx.Graph:
        """
        Query in a Belief

        :param query: Query as a graph. Use \* as an instance query.

        Example of a query [Agent:\*]-[Tell]-[Sentence:s1] will return a graph containing all agents that tell the sentence s1 in the agent belief.
        """
        if query.nodes[1]['v'] == '*':
            s = {'eq': [('c',), query.nodes[1]['c']]}
        else:
            s = {'and': [{'eq': [('c',), query.nodes[1]['c']]},
                         {'eq': [('v',), query.nodes[1]['v']]}]}
        list_p = []
        for path_crit in range(2, len(query.nodes) + 1):
            if query.nodes[path_crit]['type'] == 'c':
                if query.nodes[path_crit]['v'] == '*':
                    t = {'eq': [('c',), query.nodes[path_crit]['c']]}
                else:
                    t = {'and': [{'eq': [('c',), query.nodes[path_crit]['c']]},
                                 {'eq': [('v',), query.nodes[path_crit]['v']]}]}
            else:
                t = {'eq': [('c',), query.nodes[path_crit]['c'][0]]}
            list_p.append(PathCriteria(target=t))
        try:
            l = list(search_relationships(self.beliefs, s, *list_p))
        except RuntimeError:
            l = []
        nodes = [item for sublist in l for item in sublist]
        result = nx.subgraph(self.beliefs, nodes)
        return result

    def to_xml(self) -> Element:
        """
        Transform the Belief to XML. See :ref:`serialization` for more information.

        :return: XML version of the BaseObject
        """
        result = super().to_xml()
        data_xml = SubElement(result, 'content')
        graphml_str = ''.join(nx.generate_graphml(self.beliefs))
        data_xml.text = graphml_str
        return result

    def from_xml(self, environment, xml_node: Element):
        """
        Transform an XML to a Belief. The instance must be created before (with __init__(), passing the xml_node).
        See :ref:`serialization` for more information.

        :param environment: The environment where the BaseObject is created.
        :param xml_node: The XML node that contains the Belief data.
        """
        super().from_xml(environment=environment, xml_node=xml_node)

        for sub_object_xml in xml_node:
            if sub_object_xml.tag == 'content':
                self.beliefs = nx.parse_graphml(sub_object_xml.text, node_type=int)
