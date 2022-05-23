from typing import List, Optional, Any


class Node:
    id = 0

    def __init__(self, input_nodes_ids: List[int],
                 output_nodes_ids: Optional[List[int]] = None,
                 default_value: Optional[Any] = None):
        self.id = Node.update_id()
        self.input_nodes_ids = input_nodes_ids
        self.output_nodes_ids = output_nodes_ids
        self.value = default_value

    @classmethod
    def update_id(cls):
        cls.id += 1
        return cls.id

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
    pass
