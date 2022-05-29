"""Implementation of Node and Receptor based on Node"""
import logging
from typing import List, Optional, Any, Generator

import gin

logger = logging.getLogger()


@gin.configurable
class Node:
    id = 0

    def __init__(self, default_value: Optional[Any] = None):
        self.id = Node.update_id()
        self._input_nodes_ids = []
        self._output_nodes_ids = []
        self.value = default_value
        self.flow_calc_id = -1

    @classmethod
    def update_id(cls):
        cls.id += 1
        return cls.id

    def is_ready_to_calculate(self, graph: 'Graph', current_flow_id: int) -> bool:
        """Check input nodes values"""
        return all([graph.get_node(node_id).flow_calc_id == current_flow_id for node_id in self._input_nodes_ids])

    def calc_value(self, input_values: List[Any]) -> Any:
        raise NotImplemented("calc_value is not implemented")

    def get_input_values(self, graph: 'Graph') -> List[Any]:
        return [graph.get_node(node_id).value for node_id in self._input_nodes_ids]

    def forward_flow(self, graph: 'Graph', current_flow_id: int) -> Optional[List[int]]:
        """Calculates value and returns nodes to be processed next in the flow"""
        output_nodes_ids = [self.id]
        if self.is_ready_to_calculate(graph, current_flow_id):
            input_values = self.get_input_values(graph)
            self.value = self.calc_value(input_values)
            self.flow_calc_id = current_flow_id
            output_nodes_ids = self._output_nodes_ids
        return output_nodes_ids

    def __str__(self) -> str:
        return f"{self._input_nodes_ids};{self.id};{self._output_nodes_ids}"

    def __repr__(self) -> str:
        return f"input: {self._input_nodes_ids}; id: {self.id}; output: {self._output_nodes_ids}"


@gin.configurable
class Receptor(Node):

    def __init__(self, input_iterator: Generator[None, Any, None]):
        super().__init__(default_value=0)
        self.input_iterator = input_iterator
        self.has_stopped = False

    def calc_value(self, input_values: List[Any] = None) -> Any:
        return next(self.input_iterator)

    def forward_flow(self, graph: 'Graph', current_flow_id: int) -> Optional[List[int]]:
        self.flow_calc_id = current_flow_id
        try:
            self.value = self.calc_value()
            return self._output_nodes_ids
        except StopIteration:
            logger.info(f"Found stop iterator on receptor with {self.id=}")
            self.has_stopped = True
        return []
