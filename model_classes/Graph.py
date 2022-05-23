"""Implementation of the Graph which main function is to contain all nodes"""
from typing import List

from model_classes.Node import Node


class Graph:
    def __init__(self, input_nodes: List[Node]):
        self.all_nodes = {node.id: node for node in input_nodes}
        self.input_nodes_ids = list(self.all_nodes.keys())

    def get_node(self, node_id: int) -> Node:
        return self.all_nodes[node_id]

    def add_node(self, node: Node, is_input: bool = False):
        assert node.id not in self.all_nodes, f"Node duplicate with id = {node.id}"
        self.all_nodes[node.id] = node

        if is_input:
            self.input_nodes_ids.append(node.id)

    def delete_node(self, node_id: int):
        node_to_delete = self.all_nodes[node_id]

        if node_id in self.input_nodes_ids:
            self.input_nodes_ids.remove(node_id)

        del self.all_nodes[node_id]

        for input_node_id in node_to_delete.input_nodes_ids:
            self.all_nodes[input_node_id].remove_output_node(node_id)

        for output_node_id in node_to_delete.output_nodes_ids:
            self.all_nodes[output_node_id].remove_input_node(node_id)
