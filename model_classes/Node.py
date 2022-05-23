"""Implementation of Node and Receptor based on Node"""
import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Any, Generator

import gin

from gs_netstream import get_proxy_graph


@gin.configurable
class NodeDrawer(ABC):
    id = 0

    def __init__(self):
        self._proxy_graph = get_proxy_graph()
        self.id = NodeDrawer.update_id()

        self._proxy_graph.add_node(str(self.id))
        self.add_input_node = self.add_input_proxy_edge(self.add_input_node)
        self.add_output_node = self.add_output_proxy_edge(self.add_output_node)
        self.remove_input_node = self.del_input_proxy_edge(self.remove_input_node)
        self.remove_output_node = self.del_output_proxy_edge(self.remove_output_node)

    @classmethod
    def update_id(cls):
        cls.id += 1
        return cls.id

    @staticmethod
    def _get_edge_id(node_in: int, node_out: int) -> str:
        return f"{node_in}_{node_out}"

    def add_proxy_edge(self, node_in: int, node_out: int):
        self._proxy_graph.add_edge(self._get_edge_id(node_in, node_out), str(node_in), str(node_out))

    def del_proxy_edge(self, node_in: int, node_out: int):
        self._proxy_graph.remove_edge(self._get_edge_id(node_in, node_out))

    def add_input_proxy_edge(self, func):
        def decorator(node_id: int, *args, **kwargs):
            self.add_proxy_edge(node_id, self.id)
            return func(node_id, *args, **kwargs)
        return decorator

    def add_output_proxy_edge(self, func):
        def decorator(node_id: int, *args, **kwargs):
            self.add_proxy_edge(self.id, node_id)
            return func(node_id, *args, **kwargs)
        return decorator

    def del_input_proxy_edge(self, func):
        def decorator(node_id: int, *args, **kwargs):
            self.del_proxy_edge(node_id, self.id)
            return func(node_id, *args, **kwargs)
        return decorator

    def del_output_proxy_edge(self, func):
        def decorator(node_id: int, *args, **kwargs):
            self.del_proxy_edge(self.id, node_id)
            return func(node_id, *args, **kwargs)
        return decorator

    @abstractmethod
    def add_input_node(self, node_id: int):
        pass

    @abstractmethod
    def add_output_node(self, node_id: int):
        pass

    @abstractmethod
    def remove_input_node(self, node_id: int):
        pass

    @abstractmethod
    def remove_output_node(self, node_id: int):
        pass


class Node(NodeDrawer):

    def __init__(self, input_nodes_ids: Optional[List[int]],
                 output_nodes_ids: Optional[List[int]] = None,
                 default_value: Optional[Any] = None):
        self.input_nodes_ids = None
        self.output_nodes_ids = None
        super().__init__()
        if input_nodes_ids:
            for in_node in input_nodes_ids:
                self.add_input_node(in_node)
        if output_nodes_ids:
            for out_node in output_nodes_ids:
                self.add_output_node(out_node)
        self.value = default_value

    def add_input_node(self, node_id: int):
        #TODO: replace with Node. add output node in that node. Process duplicates in drawing
        if self.input_nodes_ids is None:
            self.input_nodes_ids = []
        self.input_nodes_ids.append(node_id)

    def add_output_node(self, node_id: int):
        if self.output_nodes_ids is None:
            self.output_nodes_ids = []
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

    def __init__(self, input_iterator: Generator[None, Any, None], *args, **kwargs):
        super().__init__(input_nodes_ids=None, default_value=0, *args, **kwargs)
        self.input_iterator = input_iterator
        self.has_stopped = False

    def forward_flow(self, graph: 'Graph') -> Optional[List[int]]:
        try:
            self.value = next(self.input_iterator)
            return self.output_nodes_ids
        except StopIteration:
            logging.info(f"Found stop iterator on receptor with {self.id=}")
            self.has_stopped = True
        return None
