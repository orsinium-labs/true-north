import math
from random import randint
import true_north

# Group is a collection of benchmarks.
# If you don't specify `name`, file name and line number will be used instead.
group = true_north.Group()


@group.add()
def math_sin(r):
    val = randint(-1000, 1000)
    for _ in r:
        math.sin(val)


if __name__ == '__main__':
    group.run().print()
