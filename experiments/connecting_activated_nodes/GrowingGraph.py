import gin

from model_classes import Graph, Node


@gin.configurable
class GrowingGraph(Graph):
    def get_output_class(self):
        pass

    def copy_node(self, node_id: int, NodeClass=Node) -> Node:
        node = self.get_node(node_id)
        node_copy = NodeClass(default_value=node.value, default_flow_id=node.flow_calc_id)

        self.add_node(node_copy, is_input=False)
        self.add_edges(node_id=node_copy.id, nodes_ids=node._input_nodes_ids, as_input=True)
        self.add_edges(node_id=node_copy.id, nodes_ids=node._output_nodes_ids, as_input=False)
        return node_copy
