import random

import gin
import argparse
import logging

from utils.data_generators import random_generator
from experiments.connecting_activated_nodes.Flow import Flow
from experiments.connecting_activated_nodes.GrowingGraph import GrowingGraph
from experiments.connecting_activated_nodes.GrowingNode import GrowingNodeReceptor

parser = argparse.ArgumentParser(description='Runs exp1 grow experiment')
parser.add_argument('--config_path', dest='config_path', action='store',
                    default=None, help='path to the .gin config')
logger = logging.getLogger()


@gin.configurable()
def set_logging_level(logging_level=logging.DEBUG):
    logger.info(f"setting logging level - {logging_level}")
    logging.basicConfig(level=logging_level)


@gin.configurable()
def create_receptor(num_iter: int):
    return GrowingNodeReceptor(random_generator(num_iter))


@gin.configurable()
def get_graph_with_input(num_of_receptors: int) -> GrowingGraph:
    receptors = [create_receptor() for _ in range(num_of_receptors)]
    return GrowingGraph(receptors)


if __name__ == '__main__':
    random.seed(1)

    args = parser.parse_args()
    if args.config_path is not None:
        gin.parse_config_file(args.config_path)

    set_logging_level()

    graph = get_graph_with_input()
    flow = Flow(graph)
    flow.run_flow()
