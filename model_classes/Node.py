"""Implementation of Node and Receptor based on Node"""
import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Any, Generator

from gs_netstream import NetStreamProxyGraph


class NodeDrawer(ABC):
    id = 0

    def __init__(self, proxy_graph: NetStreamProxyGraph):
        self.__proxy_graph = proxy_graph
        self.id = Node.update_id()

        self.__proxy_graph.add_node(str(self.id))
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
        self.__proxy_graph.add_edge(self._get_edge_id(node_in, node_out), str(node_in), str(node_out))

    def del_proxy_edge(self, node_in: int, node_out: int):
        self.__proxy_graph.remove_edge(self._get_edge_id(node_in, node_out))

    @staticmethod
    def add_input_proxy_edge(func):
        def decorator(self, node_id: int, *args, **kwargs):
            self.add_proxy_edge(node_id, self.id)
            return func(self, node_id, *args, **kwargs)
        return decorator

    @staticmethod
    def add_output_proxy_edge(func):
        def decorator(self, node_id: int, *args, **kwargs):
            self.add_proxy_edge(self.id, node_id)
            return func(self, node_id, *args, **kwargs)
        return decorator

    @staticmethod
    def del_input_proxy_edge(func):
        def decorator(self, node_id: int, *args, **kwargs):
            self.del_proxy_edge(node_id, self.id)
            return func(self, node_id, *args, **kwargs)
        return decorator

    @staticmethod
    def del_output_proxy_edge(func):
        def decorator(self, node_id: int, *args, **kwargs):
            self.del_proxy_edge(self.id, node_id)
            return func(self, node_id, *args, **kwargs)
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

    def __init__(self, input_nodes_ids: List[int],
                 output_nodes_ids: Optional[List[int]] = None,
                 default_value: Optional[Any] = None,
                 *args, **kwargs):
        assert isinstance(input_nodes_ids, list) and len(input_nodes_ids) > 0,\
            f"incorrect input nodes ids = {input_nodes_ids}"
        self.input_nodes_ids = input_nodes_ids
        self.output_nodes_ids = output_nodes_ids
        self.value = default_value
        super().__init__(*args, **kwargs)

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

    def __init__(self, input_iterator: Generator[Any], output_nodes_ids: List[int], *args, **kwargs):
        assert isinstance(output_nodes_ids, list) and len(output_nodes_ids) > 0, \
            f"incorrect output nodes for receptor {output_nodes_ids=}"
        super().__init__(input_nodes_ids=[0], *args, **kwargs)
        self.input_iterator = input_iterator
        self.input_nodes_ids = None

    def forward_flow(self, graph: 'Graph') -> Optional[List[int]]:
        try:
            self.value = next(self.input_iterator)
            return self.output_nodes_ids
        except StopIteration:
            logging.info(f"Found stop iterator on receptor with {self.id=}")
        return None
