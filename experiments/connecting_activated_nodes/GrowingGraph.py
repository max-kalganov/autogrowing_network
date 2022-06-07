from typing import List

import gin

from experiments.connecting_activated_nodes import GrowingNode
from model_classes import Graph, Node


@gin.configurable
class GrowingGraph(Graph):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._leafs = set()

    def add_leaf(self, node_id: int):
        self._leafs.add(node_id)

    def clear_leafs(self):
        self._leafs = set()

    def add_leaf_node(self, input_nodes: List[int]) -> int:
        new_node = GrowingNode()
        self.add_node(new_node)
        self.add_edges(node_id=new_node.id, nodes_ids=input_nodes, as_input=True)
        return new_node.id

    def grow_receptors(self):
        receptors_leafs = set(leaf_id for leaf_id in self._leafs if leaf_id in self.input_nodes_ids)
        self._leafs = self._leafs - receptors_leafs
        new_rec_leafs_ids = set(self.add_leaf_node([receptor_id]) for receptor_id in receptors_leafs)
        for rec_leaf_id in new_rec_leafs_ids:
            leaf_node = self.get_node(rec_leaf_id)
            input_values = leaf_node.get_input_values(self)
            assert len(input_values) == 1, f"incorrect number of input nodes when growing receptors"
            leaf_node.value = input_values[0]

        self._leafs.update(new_rec_leafs_ids)

    def connect_leafs(self):
        self.grow_receptors()

        active_leafs = set(leaf_id for leaf_id in self._leafs if self.get_node(leaf_id).is_active())
        if len(active_leafs) > 1:
            leaf_node_id = self.add_leaf_node(list(active_leafs))
            self._leafs = {leaf_node_id}

    def get_output_class(self):
        output_classes = []
        for node_id, node in self.all_nodes.items():
            if node.value > 0:
                output_classes.append(str(node_id))
        return '|'.join(output_classes)

    def copy_node(self, node_id: int, NodeClass=Node) -> Node:
        node = self.get_node(node_id)
        node_copy = NodeClass(default_value=node.value, default_flow_id=node.flow_calc_id)

        self.add_node(node_copy, is_input=False)
        self.add_edges(node_id=node_copy.id, nodes_ids=node._input_nodes_ids, as_input=True)
        self.add_edges(node_id=node_copy.id, nodes_ids=node._output_nodes_ids, as_input=False)
        return node_copy

    def add_node_with_edges(self, node: Node, input_nodes_ids: List[int], output_nodes_ids: List[int]):
        self.add_node(node, is_input=False)
        self.add_edges(node_id=node.id, nodes_ids=input_nodes_ids, as_input=True)
        self.add_edges(node_id=node.id, nodes_ids=output_nodes_ids, as_input=False)
