import math
from random import randint
import true_north

# Group is a collection of benchmarks.
# If you don't specify `name`, file name and line number will be used instead.
group = true_north.Group()


# Register as many benchmarks as you need by decorating them with `@group.add()`.
@group.add()
def math_sin(r):
    # Before the loop, you can setup anything you need
    # for the benchmarked code to work. This setup won't be included
    # in the resulting timing.
    val = randint(-1000, 1000)
    # The timer start as soon as the code enters the loop.
    for _ in r:
        math.sin(val)
    # The timer stops as soon as the code exits the loop.


if __name__ == '__main__':
    group.print()
