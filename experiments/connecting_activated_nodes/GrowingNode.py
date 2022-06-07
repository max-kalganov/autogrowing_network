from collections import defaultdict
from copy import copy
from typing import List, Optional, Union

import gin

from model_classes import Node, Receptor
import logging

logger = logging.getLogger()


@gin.configurable
class GrowingNode(Node):
    def __init__(self, activation_limit: float = 0.5, default_value=0, active_count: int = 5,
                 inactive_count: int = 5, max_duplicates: int = 3, *args, **kwargs):
        super().__init__(default_value, *args, **kwargs)
        self._activation_limit = activation_limit
        self._active_count = active_count
        self._default_active_count = active_count
        self._inactive_count = inactive_count
        self._default_inactive_count = inactive_count
        self._make_duplicate_flow_id = None
        self._duplicate_left = max_duplicates
        self._input_nodes_values = defaultdict(int)
        self._value_sum = 0

    def is_active(self) -> bool:
        return self.is_active_value(self.value, self._activation_limit)

    @staticmethod
    def is_active_value(value: float, activation_limit: float):
        return value > activation_limit

    def calc_value(self, node: Union['GrowingNodeReceptor', 'GrowingNode'], node_id_from: int) -> float:
        stored_node_value = self._input_nodes_values[node_id_from]
        node_value = node.value
        self._value_sum -= stored_node_value
        self._value_sum += node_value
        self._input_nodes_values[node_id_from] = node_value
        return self._value_sum / len(self._input_nodes_values)

    def _process_active_value(self, graph):
        if self._active_count <= 0:
            node_copy = GrowingNode(default_value=0, default_flow_id=self.flow_calc_id)

            graph.add_node_with_edges(
                node_copy,
                input_nodes_ids=[node_id for node_id in self._input_nodes_ids if node_id in graph.input_nodes_ids
                                 or graph.get_node(node_id).is_active()],
                output_nodes_ids=copy(self._output_nodes_ids)
            )
            self._active_count = self._default_active_count
            self._duplicate_left -= 1
        else:
            self._active_count -= 1

        self._inactive_count = self._default_inactive_count

    def _process_inactive_value(self, graph, current_flow_id: int):
        self._inactive_count -= (current_flow_id - self.flow_calc_id + 1)
        if self._inactive_count <= 0:
            logger.info("Deleting inactive node")
            graph.delete_node(self.id)
        else:
            self._inactive_count -= 1
        self._active_count = self._default_active_count

    def _process_inputs(self, graph: 'GrowingGraph', current_flow_id: int, node_id_from: int) -> Union[int, List[int], None]:
        prev_state = self.is_active()
        prev_value = self.value
        self.value = self.calc_value(graph.get_node(node_id_from), node_id_from)
        output_nodes_ids = self._output_nodes_ids if self.is_active() and prev_value != self.value else -1
        if prev_state != self.is_active():
            if self.is_active():
                self._process_active_value(graph)
            else:
                self._process_inactive_value(graph, current_flow_id)

        if self._duplicate_left == 0:
            graph.delete_node(self.id)
            output_nodes_ids = -1
        self.flow_calc_id = current_flow_id
        return output_nodes_ids

    def forward_flow(self, graph: 'GrowingGraph', current_flow_id: int, node_id_from: int) -> Optional[List[int]]:
        """Calculates value and returns nodes to be processed next in the flow"""
        if self.flow_calc_id != current_flow_id:
            self.value = 0
            self._value_sum = 0
            self._input_nodes_values = defaultdict(int)
        return self._process_inputs(graph, current_flow_id, node_id_from)


class GrowingNodeReceptor(Receptor):
    def forward_flow(self, graph: 'Graph', current_flow_id: int, prev_node: int) -> Optional[List[int]]:
        self.flow_calc_id = current_flow_id
        try:
            self.value = self.calc_value()
            return self._output_nodes_ids
        except StopIteration:
            logger.info(f"Found stop iterator on receptor with {self.id=}")
            self.has_stopped = True
        return []
