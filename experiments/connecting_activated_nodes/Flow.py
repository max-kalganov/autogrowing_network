import gin

from experiments.connecting_activated_nodes.GrowingNode import GrowingNode
from model_classes import BaseFlow

import logging
logger = logging.getLogger()


@gin.configurable
class Flow(BaseFlow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._all_leafs = []

    def run_single_flow(self):
        self.fill_started_nodes_deque()
        while len(self._nodes_flow_deque) > 0:
            node_id = self._nodes_flow_deque.popleft()
            if node_id not in self.graph.all_nodes:
                continue

            node = self.graph.get_node(node_id)
            output_nodes_ids = node.forward_flow(self.graph, self.current_flow_num)
            if output_nodes_ids == -1:
                continue
            elif len(output_nodes_ids) > 0:
                self.append_to_nodes_deque(output_nodes_ids)
            else:
                self.process_leaf(node_id)

    def connect_leafs(self):
        active_leafs = set()
        for leaf_id in self._all_leafs:
            leaf: GrowingNode = self.graph.get_node(leaf_id)
            if leaf_id in self.graph.input_nodes_ids or leaf.is_active():
                active_leafs.add(leaf_id)

        if len(active_leafs) > 1:
            new_node = GrowingNode()
            self.graph.add_node(new_node)
            self.graph.add_edges(node_id=new_node.id, nodes_ids=list(active_leafs), as_input=True)
        self._all_leafs = []

    def run_flow(self) -> None:
        while not self.is_flow_completed():
            logger.info(f"Running iteration = {self.current_flow_num}")
            self.run_single_flow()
            self.connect_leafs()
            self.current_flow_num += 1

    def process_leaf(self, node_id: int):
        self._all_leafs.append(node_id)
