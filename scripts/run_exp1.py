import random

from experiments.connecting_activated_nodes import GrowingNode
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
        rval = random.random()
        yield rval


if __name__ == '__main__':
    args = parser.parse_args()
    if args.config_path is not None:
        gin.parse_config_file(args.config_path)
    num_iter = 100
    rec1, node1 = Receptor(random_generator(num_iter)), GrowingNode()
    rec2, node2 = Receptor(random_generator(num_iter)), GrowingNode()
    rec3, node3 = Receptor(random_generator(num_iter)), GrowingNode()
    input_nodes = [rec1, rec2, rec3]
    graph = GrowingGraph(input_nodes)
    graph.add_node(node1)
    graph.add_node(node2)
    graph.add_node(node3)

    graph.add_edge(rec1.id, node1.id)
    graph.add_edge(rec2.id, node2.id)
    graph.add_edge(rec3.id, node3.id)

    flow = Flow(graph)
    flow.run_flow()
