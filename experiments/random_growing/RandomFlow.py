"""Implementation of the basic Flow which can fill the Graph and run the Flow"""
import random

from experiments.random_growing.RandomNode import RandomNode
from model_classes import BaseFlow


class RandomFlow(BaseFlow):
    def process_leaf(self, node_id: int):
        """Process node without output"""
        # input_nodes = random.choices(list(self.graph.all_nodes.keys()), k=2)
        input_nodes = [node_id]#  + list(set(input_nodes) - {node_id})
        rnode = RandomNode(input_nodes)
        self.graph.add_node(rnode)
