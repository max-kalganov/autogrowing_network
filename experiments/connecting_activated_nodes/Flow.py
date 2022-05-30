import gin

from model_classes import BaseFlow


@gin.configurable
class Flow(BaseFlow):
    def run_single_flow(self):
        self.fill_started_nodes_deque()
        while len(self._nodes_flow_deque) > 0:
            node_id = self._nodes_flow_deque.popleft()
            node = self.graph.get_node(node_id)
            output_nodes_ids = node.forward_flow(self.graph, self.current_flow_num)
            if output_nodes_ids == -1:
                continue
            elif len(output_nodes_ids) > 0:
                self.append_to_nodes_deque(output_nodes_ids)
            else:
                self.process_leaf(node_id)
