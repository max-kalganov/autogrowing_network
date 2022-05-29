import random

import gin


@gin.configurable("DataGenerator")
def example_data_generator(num_test_sameples: int = 10):
    for i in range(num_test_sameples):
        yield int(random.random() > 0.5)
