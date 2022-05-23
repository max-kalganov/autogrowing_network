"""Implementation of the basic Flow which can fill the Graph and run the Flow"""
import random

from experiments.random_growing.RandomNode import RandomNode
from model_classes import BaseFlow


class RandomFlow(BaseFlow):
    def run_flow(self):
        self.fill_started_nodes_deque()
        for node_id in self._nodes_flow_deque.popleft():
            node = self.graph.get_node(node_id)
            output_nodes_ids = node.forward_flow(self.graph)
            if output_nodes_ids is not None:
                self.append_to_nodes_deque(output_nodes_ids)
            else:
                self.process_leaf(node_id)

    def process_leaf(self, node_id: int):
        """Process node without output"""
        input_nodes = random.choices(list(self.graph.all_nodes.keys()), k=2)
        input_nodes = [node_id] + list(set(input_nodes) - {node_id})
        rnode = RandomNode(input_nodes)
        self.graph.add_node(rnode)
