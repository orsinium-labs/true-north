from random import randint
import true_north


group = true_north.Group()


@group.add()
def sort_method():
    with true_north.setup():
        a = [randint(-1000, 1000) for _ in range(1000)]
    a.sort()


@group.add()
def sorted_function():
    with true_north.setup():
        a = [randint(-1000, 1000) for _ in range(1000)]
    sorted(a)


if __name__ == '__main__':
    group.run().print()
