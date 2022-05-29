import gin

from model_classes import Graph


@gin.configurable
class ExampleGraph(Graph):
    def get_output_class(self):
        output_classes = []
        for node_id, node in self.all_nodes.items():
            if node.value > 0:
                output_classes.append(str(node_id))
        return '|'.join(output_classes)


@gin.configurable
class IncorrectExampleGraph(Graph):
    def get_output_class(self):
        output_class = 0
        for node_id, node in self.all_nodes.items():
            if node.value > 0:
                output_class += 1
        return output_class
