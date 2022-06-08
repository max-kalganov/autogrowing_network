import random

import gin


@gin.configurable()
def random_generator(number_of_values: int):
    for i in range(number_of_values):
        yield random.random()
