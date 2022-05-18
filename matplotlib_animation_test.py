import numpy as np
from matplotlib import pyplot as plt
from IPython.display import clear_output
from time import sleep
from pyvis.network import Network
import networkx as nx

def draw_func(val):
    nt.add_node(val)
    if val != 0:
        nt.add_edge(val - 1, val)
    nx.draw(nt)

nt = nx.Graph()
plt.figure()

if __name__ == '__main__':
    try:
        for i in range(100):
            draw_func(i)
            plt.show()
            if 0.1:
                sleep(0.1)
            clear_output(wait=True)
        draw_func(100)
        plt.show()
    except KeyboardInterrupt:
        pass
