"""Implementation of the basic Flow which can fill the Graph and run the Flow"""
import random

from experiments.random_growing.RandomNode import RandomNode
from model_classes import BaseFlow


class RandomFlow(BaseFlow):
    def run_single_flow(self):
        self.fill_started_nodes_deque()
        ignore_nodes = set()
        while len(self._nodes_flow_deque) > 0:
            node_id = self._nodes_flow_deque.popleft()
            if node_id in ignore_nodes:
                continue
            node = self.graph.get_node(node_id)
            output_nodes_ids = node.forward_flow(self.graph, self.current_flow_num)
            if len(output_nodes_ids) > 0:
                self.append_to_nodes_deque(output_nodes_ids)
            else:
                ignore_nodes.add(self.process_leaf(node_id))

    def process_leaf(self, node_id: int):
        """Process node without output"""
        input_nodes = random.choices(list(self.graph.all_nodes.keys()), k=5)
        input_nodes = [node_id] + list(set(input_nodes) - {node_id})
        rnode = RandomNode()
        self.graph.add_node(rnode)
        self.graph.add_edges(node_id=rnode.id, nodes_ids=input_nodes, as_input=True)
        return rnode.id
