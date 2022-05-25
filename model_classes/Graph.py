"""Implementation of the Graph which main function is to contain all nodes"""
from typing import List

from gs_netstream import NetStreamProxyGraph
from model_classes.Node import Node, Receptor


class Graph:
    def __init__(self, input_nodes: List[Receptor]):
        self.all_nodes = {node.id: node for node in input_nodes}
        self.input_nodes_ids = list(self.all_nodes.keys())
        self.__proxy_graph = NetStreamProxyGraph()

    @staticmethod
    def _get_edge_draw_id(node_in: int, node_out: int) -> str:
        return f"{node_in}_{node_out}"

    @staticmethod
    def _get_node_draw_id(node_id: int) -> str:
        return str(node_id)

    def get_node(self, node_id: int) -> Node:
        return self.all_nodes[node_id]

    def add_node(self, node: Node, is_input: bool = False):
        assert node.id not in self.all_nodes, f"Node duplicate with id = {node.id}"
        assert node._input_nodes_ids == [] and node._output_nodes_ids == [], \
            f"not empty input-output node ids in node {node}"

        self.all_nodes[node.id] = node
        self.__proxy_graph.add_node(self._get_node_draw_id(node_id=node.id))

        if is_input:
            self.input_nodes_ids.append(node.id)

    def delete_node(self, node_id: int):
        assert node_id in self.all_nodes, f"Node with id = {node_id} not found"
        node_to_delete = self.all_nodes[node_id]

        if node_id in self.input_nodes_ids:
            self.input_nodes_ids.remove(node_id)

        for input_node_id in node_to_delete._input_nodes_ids:
            self.del_edge(input_node_id, node_id)

        for output_node_id in node_to_delete._output_nodes_ids:
            self.del_edge(node_id, output_node_id)

        del self.all_nodes[node_id]
        self.__proxy_graph.remove_node(self._get_node_draw_id(node_id))

    def add_edge(self, in_node_id: int, out_node_id: int):
        assert in_node_id in self.all_nodes and out_node_id in self.all_nodes, \
            f"nodes {in_node_id, out_node_id} not found in graph nodes"

        in_node = self.get_node(in_node_id)
        out_node = self.get_node(out_node_id)

        in_node._output_nodes_ids.append(out_node_id)
        out_node._input_nodes_ids.append(in_node_id)

        self.add_proxy_edge(in_node_id, out_node_id)

    def del_edge(self, in_node_id: int, out_node_id: int):
        assert in_node_id in self.all_nodes and out_node_id in self.all_nodes, \
            f"nodes {in_node_id, out_node_id} not found in graph nodes"

        in_node = self.get_node(in_node_id)
        out_node = self.get_node(out_node_id)

        in_node._output_nodes_ids.remove(out_node_id)
        out_node._input_nodes_ids.remove(in_node_id)

        self.del_proxy_edge(in_node_id, out_node_id)

    def add_proxy_edge(self, node_in: int, node_out: int):
        self.__proxy_graph.add_edge(self._get_edge_draw_id(node_in, node_out), str(node_in), str(node_out))

    def del_proxy_edge(self, node_in: int, node_out: int):
        self.__proxy_graph.remove_edge(self._get_edge_draw_id(node_in, node_out))
