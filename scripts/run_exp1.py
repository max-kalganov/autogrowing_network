import random
from typing import List, Tuple

from experiments.connecting_activated_nodes import GrowingNode
from experiments.connecting_activated_nodes.Flow import Flow
from experiments.connecting_activated_nodes.GrowingGraph import GrowingGraph
from experiments.connecting_activated_nodes.GrowingNode import GrowingNodeReceptor
import gin
import argparse
import logging

parser = argparse.ArgumentParser(description='Runs exp1 grow experiment')
parser.add_argument('--config_path', dest='config_path', action='store',
                    default=None, help='path to the .gin config')
logger = logging.getLogger()


@gin.configurable()
def set_logging_level(logging_level = logging.DEBUG):
    logger.info(f"setting logging level - {logging_level}")
    logging.basicConfig(level=logging_level)


def random_generator(number_of_values):
    for i in range(number_of_values):
        rval = random.random()
        yield rval


def create_receptor_with_node():
    return GrowingNodeReceptor(random_generator(num_iter)), GrowingNode()


def add_input_to_graph(receptors_with_nodes: List[Tuple[GrowingNodeReceptor, GrowingNode]]) -> GrowingGraph:
    input_nodes = [rec for rec, node in receptors_with_nodes]
    graph = GrowingGraph(input_nodes)

    for rec, node in receptors_with_nodes:
        graph.add_node(node)
        graph.add_edge(rec.id, node.id)
    return graph


if __name__ == '__main__':
    random.seed(1)

    args = parser.parse_args()
    if args.config_path is not None:
        gin.parse_config_file(args.config_path)

    set_logging_level()

    num_iter = 100
    num_of_receptors = 20
    receptors_with_nodes = [create_receptor_with_node() for i in range(num_of_receptors)]
    graph = add_input_to_graph(receptors_with_nodes)

    flow = Flow(graph)
    flow.run_flow()
