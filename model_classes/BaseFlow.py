"""Implementation of the basic Flow which can fill the Graph and run the Flow"""
from collections import deque
from typing import List

from model_classes.Graph import Graph


class BaseFlow:
    def __init__(self, graph: Graph):
        self.graph = graph
        self._nodes_flow_deque = deque()

    def fill_started_nodes_deque(self):
        self.append_to_nodes_deque(self.graph.input_nodes_ids)

    def append_to_nodes_deque(self, nodes_ids: List[int]):
        for node_id in nodes_ids:
            self._nodes_flow_deque.append(node_id)

    def run_single_flow(self):
        self.fill_started_nodes_deque()
        while len(self._nodes_flow_deque) > 0:
            node_id = self._nodes_flow_deque.popleft()
            node = self.graph.get_node(node_id)
            output_nodes_ids = node.forward_flow(self.graph)
            if output_nodes_ids is not None:
                self.append_to_nodes_deque(output_nodes_ids)
            else:
                self.process_leaf(node_id)

    def run_flow(self):
        while any([self.graph.get_node(in_node_id).has_stopped is False for in_node_id in self.graph.input_nodes_ids]):
            self.run_single_flow()

    def process_leaf(self, node_id: int):
        """Process node without output"""
