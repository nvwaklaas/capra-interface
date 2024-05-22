"""Route Class in Capra Hircus format"""

from edge import Edge
from node import Node
from interfaces.route_abc import RouteAbstractClass


class CapraRoute(RouteAbstractClass):
    """Class for defining a route in Capra Hircus format"""

    def __init__(self, path_uuid, path_encoding=0) -> None:
        self.path_uuid = path_uuid
        self.path_encoding = path_encoding
        self.nodes = []
        self.edges = []

    def add_node(self, node: Node) -> None:
        """Adds a node to the route"""

        self.nodes.append(
            node.get_formatted_node()
        )

    def add_edge(self, edge: Edge) -> None:
        """Adds an edge to the route"""

        self.edges.append(
            edge.get_formatted_edge()
        )

    def get_formatted_route(self) -> dict:
        """Returns a route in the correct format for Capra Hircus"""

        return {
            "path_uuid": self.path_uuid,
            "path_encoding": self.path_encoding,
            "nodes": self.nodes,
            "edges": self.edges
        }
