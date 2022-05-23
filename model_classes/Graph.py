"""Implementation of the Graph which main function is to contain all nodes"""
from typing import List

from model_classes.Node import Node


class Graph:
    def __init__(self, input_nodes: List[Node]):
        self.all_nodes = {node.id: node for node in input_nodes}
        self.input_nodes_ids = list(self.all_nodes.keys())

    def add_node(self, node: Node, is_input: bool = False):
        assert node.id not in self.all_nodes, f"Node duplicate with id = {node.id}"
        self.all_nodes[node.id] = node

        if is_input:
            self.input_nodes_ids.append(node.id)

    def delete_node(self, node_id: int):
        if node_id in self.input_nodes_ids:
            self.input_nodes_ids.remove(node_id)

        del self.all_nodes[node_id]
