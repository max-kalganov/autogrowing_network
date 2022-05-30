import random
from typing import Dict, List, Optional

import gin

from model_classes import Node
import logging
logger = logging.getLogger()


@gin.configurable
class GrowingNode(Node):
    def __init__(self, activation_limit: float = 0.5, default_value=0, inactive_count: int = 5):
        super().__init__(default_value)
        self._straight_connections: Dict[int, float] = {}
        self._activation_limit = activation_limit
        self._inactive_count = inactive_count
        self._default_inactive_count = inactive_count

    def _has_straight_connection(self, graph: 'Graph', current_flow_id: int) -> bool:
        return any([(graph.get_node(node_id).flow_calc_id == current_flow_id
                     and graph.get_node(node_id).value > self._activation_limit) for node_id in self._straight_connections])

    def _are_input_nodes_activated(self, graph: 'Graph', current_flow_id: int) -> bool:
        return all([graph.get_node(node_id).flow_calc_id == current_flow_id for node_id in self._input_nodes_ids])

    def is_active(self) -> bool:
        return self.value > self._activation_limit

    def calc_value(self, input_values: List[float]) -> float:
        raise NotImplemented("calc_value is not implemented")

    def forward_flow(self, graph: 'GrowingGraph', current_flow_id: int) -> Optional[List[int]]:
        """Calculates value and returns nodes to be processed next in the flow"""
        output_nodes_ids = [self.id]
        if self._has_straight_connection(graph, current_flow_id):
            raise NotImplemented("Implement straight connections")
        elif self._are_input_nodes_activated(graph, current_flow_id):
            input_values = self.get_input_values(graph)
            self.value = self.calc_value(input_values)
            self.flow_calc_id = current_flow_id
            output_nodes_ids = self._output_nodes_ids
            if self.is_active():
                graph.copy_node(self.id, GrowingNode)
                self._inactive_count = self._default_inactive_count
            else:
                if self._inactive_count > 0:
                    logger.info("Deleting inactive node")
                    graph.delete_node(self.id)
                    output_nodes_ids = -1
                self._inactive_count -= 1
        return output_nodes_ids
