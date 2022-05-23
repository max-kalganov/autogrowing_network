import logging
from typing import List, Optional, Any, Generator


class Node:
    id = 0

    def __init__(self, input_nodes_ids: List[int],
                 output_nodes_ids: Optional[List[int]] = None,
                 default_value: Optional[Any] = None):
        assert isinstance(input_nodes_ids, list) and len(input_nodes_ids) > 0,\
            f"incorrect input nodes ids = {input_nodes_ids}"
        self.id = Node.update_id()
        self.input_nodes_ids = input_nodes_ids
        self.output_nodes_ids = output_nodes_ids
        self.value = default_value

    @classmethod
    def update_id(cls):
        cls.id += 1
        return cls.id

    def add_input_node(self, node_id: int):
        self.input_nodes_ids.append(node_id)

    def add_output_node(self, node_id: int):
        self.output_nodes_ids.append(node_id)

    def remove_input_node(self, node_id: int):
        assert node_id in self.input_nodes_ids and len(self.input_nodes_ids) > 1, "can not remove input node"
        self.input_nodes_ids.remove(node_id)

    def remove_output_node(self, node_id: int):
        assert node_id in self.output_nodes_ids, "can not remove output node"
        self.output_nodes_ids.remove(node_id)

    def is_ready_to_calculate(self, graph: 'Graph') -> bool:
        """Check input nodes values"""
        return all([graph.all_nodes[node_id].value is not None for node_id in self.input_nodes_ids])

    def calc_value(self, input_values: List[Any]) -> Any:
        raise NotImplemented("calc_value is not implemented")

    def get_input_values(self, graph: 'Graph') -> List[Any]:
        return [graph.all_nodes[node_id].value for node_id in self.input_nodes_ids]

    def forward_flow(self, graph: 'Graph') -> Optional[List[int]]:
        """Calculates value and returns nodes to be processed next in the flow"""
        output_nodes_ids = [self.id]
        if self.is_ready_to_calculate(graph):
            input_values = self.get_input_values(graph)
            self.value = self.calc_value(input_values)
            output_nodes_ids = self.output_nodes_ids
        return output_nodes_ids


class Receptor(Node):

    def __init(self, input_iterator: Generator[Any], output_nodes_ids: List[int]):
        assert isinstance(output_nodes_ids, list) and len(output_nodes_ids) > 0, \
            f"incorrect output nodes for receptor {output_nodes_ids=}"
        super().__init__(input_nodes_ids=[0])
        self.input_iterator = input_iterator
        self.input_nodes_ids = None

    def forward_flow(self, graph: 'Graph') -> Optional[List[int]]:
        try:
            self.value = next(self.input_iterator)
            return self.output_nodes_ids
        except StopIteration:
            logging.info(f"Found stop iterator on receptor with {self.id=}")
        return None
