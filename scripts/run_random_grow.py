import random

from experiments.random_growing.RandomFlow import RandomFlow
from model_classes import Receptor, Graph
import gin
import argparse

parser = argparse.ArgumentParser(description='Runs random grow experiment')
parser.add_argument('--config_path', dest='config_path', action='store',
                    default=None, help='path to the .gin config')


def random_generator(number_of_values):
    for i in range(number_of_values):
        yield random.random()
    yield None


if __name__ == '__main__':
    args = parser.parse_args()

    gin.parse_config_file(args.config_path)
    input_nodes = [Receptor(random_generator(10)), Receptor(random_generator(10))]
    graph = Graph(input_nodes)
    flow = RandomFlow(graph)
    flow.run_flow()
