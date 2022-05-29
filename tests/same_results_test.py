import os
from dataclasses import dataclass
import unittest

import gin

from model_classes import BaseFlow, Graph
from tests.test_constants import TEST_CONFIG_PATH_VAR


@gin.configurable
@dataclass
class SameResultsTestConf:
    FLOW: BaseFlow
    PRINT_RESULTS: bool = False


class SameResultsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config_path = os.environ.get(TEST_CONFIG_PATH_VAR, None)
        assert config_path is not None, f"set {TEST_CONFIG_PATH_VAR} in environment variables"
        gin.parse_config_file(config_path)
        cls.test_config = SameResultsTestConf()

    def test_exp_has_corresponding_method(self):
        self.assertIn("get_output_class", dir(self.test_config.FLOW.graph),
                      "graph doesn't have method 'get_output_class' for the input")

    @staticmethod
    def _get_node_values_id(graph: Graph):
        return tuple(graph.get_node(input_node_id).value for input_node_id in graph.input_nodes_ids)

    def test_same_results(self):
        self.assertGreater(len(self.test_config.FLOW.graph.input_nodes_ids), 0,
                           f"graph is not filled with input nodes")

        input_to_output = {}
        output_to_input = {}
        input_number = 0
        while not self.test_config.FLOW.is_flow_completed():
            with self.subTest(f"input number: {input_number}"):
                self.test_config.FLOW.run_single_flow()
                node_values_id = self._get_node_values_id(self.test_config.FLOW.graph)
                output_class = self.test_config.FLOW.graph.get_output_class()
                print(f"{node_values_id=} -- {output_class=}")
                if node_values_id in input_to_output:
                    self.assertEqual(output_class, input_to_output[node_values_id],
                                     f"different output results for the same input "
                                     f"({node_values_id=}, {output_class=} "
                                     f"| previous output = {input_to_output[node_values_id]})")
                else:
                    input_to_output[node_values_id] = output_class

                if output_class in output_to_input:
                    self.assertEqual(node_values_id, output_to_input[output_class],
                                     f"several inputs have one output result"
                                     f"({node_values_id=}, {output_class=} "
                                     f"| another input = {output_to_input[output_class]})")
                else:
                    output_to_input[output_class] = node_values_id
