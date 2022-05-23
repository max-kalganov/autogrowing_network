"""Implementation of Node and Receptor based on Node"""
from typing import List, Any
from random import random
from model_classes import Node


class RandomNode(Node):
    def calc_value(self, input_values: List[Any]) -> Any:
        self.value = random()
