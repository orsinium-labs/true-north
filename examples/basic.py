import math
from random import randint

import true_north


# Group is a collection of benchmarks.
# If you don't specify `name`, file name and line number will be used instead.
group = true_north.Group()


# Register as many benchmarks as you need by decorating them with `@group.add()`.
@group.add
def math_sin(r):
    # Before the loop, you can setup anything you need
    # for the benchmarked code to work. This setup won't be included
    # in the resulting timing.
    val = randint(-1000, 1000)
    # The timer start as soon as the code enters the loop.
    for _ in r:
        math.sin(val)
    # The timer stops as soon as the code exits the loop.


# The decorator accepts some cool arguments,
# just check out the docstring. The most useful one is `name`.
@group.add(name='math.cos')
# Since we explicitly specified a nice name for the benchmark,
# the function name doesn't matter, we can just omit it.
def _(r):
    val = randint(-1000, 1000)
    for _ in r:
        math.cos(val)


@group.add(name='math.tan')
def _(r):
    val = randint(-1000, 1000)
    for _ in r:
        math.tan(val)


# We hide the group execution under this `if` block,
# so we can execute the benchmark using CLI (`python3 -m true_north`).
if __name__ == '__main__':
    # If the script is run directly (`python3 examples/basic.py`),
    # run and print benchmarks.
    group.print()
