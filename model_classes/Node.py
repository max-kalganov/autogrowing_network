"""Implementation of Node and Receptor based on Node"""
import logging
from typing import List, Optional, Any, Generator


class Node:
    id = 0

    def __init__(self, default_value: Optional[Any] = None):
        self.id = Node.update_id()
        self.__input_nodes_ids = []
        self.__output_nodes_ids = []
        self.value = default_value

    @classmethod
    def update_id(cls):
        cls.id += 1
        return cls.id

    def is_ready_to_calculate(self, graph: 'Graph') -> bool:
        """Check input nodes values"""
        return all([graph.all_nodes[node_id].value is not None for node_id in self.__input_nodes_ids])

    def calc_value(self, input_values: List[Any]) -> Any:
        raise NotImplemented("calc_value is not implemented")

    def get_input_values(self, graph: 'Graph') -> List[Any]:
        return [graph.all_nodes[node_id].value for node_id in self.__input_nodes_ids]

    def forward_flow(self, graph: 'Graph') -> Optional[List[int]]:
        """Calculates value and returns nodes to be processed next in the flow"""
        output_nodes_ids = [self.id]
        if self.is_ready_to_calculate(graph):
            input_values = self.get_input_values(graph)
            self.value = self.calc_value(input_values)
            output_nodes_ids = self.__output_nodes_ids
        return output_nodes_ids


class Receptor(Node):

    def __init__(self, input_iterator: Generator[None, Any, None]):
        super().__init__(default_value=0)
        self.input_iterator = input_iterator
        self.has_stopped = False

    def forward_flow(self, graph: 'Graph') -> Optional[List[int]]:
        try:
            self.value = next(self.input_iterator)
            return self.__output_nodes_ids
        except StopIteration:
            logging.info(f"Found stop iterator on receptor with {self.id=}")
            self.has_stopped = True
        return None
