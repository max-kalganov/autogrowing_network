import random

from experiments.connecting_activated_nodes.Flow import Flow
from experiments.connecting_activated_nodes.GrowingGraph import GrowingGraph
from model_classes import Receptor
import gin
import argparse
import logging

parser = argparse.ArgumentParser(description='Runs exp1 grow experiment')
parser.add_argument('--config_path', dest='config_path', action='store',
                    default=None, help='path to the .gin config')
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


def random_generator(number_of_values):
    for i in range(number_of_values):
        yield random.random() > 0.5


if __name__ == '__main__':
    args = parser.parse_args()
    if args.config_path is not None:
        gin.parse_config_file(args.config_path)
    num_iter = 10
    input_nodes = [Receptor(random_generator(num_iter)),
                   Receptor(random_generator(num_iter)),
                   Receptor(random_generator(num_iter))]
    graph = GrowingGraph(input_nodes)
    flow = Flow(graph)
    flow.run_flow()
