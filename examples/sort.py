import heapq
from random import randint
import true_north


def random_list() -> list:
    return [randint(-1000, 1000) for _ in range(1000)]


def insert_sort(values: list) -> list:
    for i, vi in enumerate(values):
        for j, vj in enumerate(values):
            if vi < vj:
                values[i], values[j] = vj, vi
                vi = values[i]
    return values


def select_sort(values: list) -> list:
    result = []
    while values:
        m = min(enumerate(values), key=lambda x: x[1])
        del values[m[0]]
        result.append(m[1])
    return result


def bubble_sort(values: list) -> list:
    n = len(values)
    for i in range(n, 0, -1):
        for j in range(n - i - 1, 0, -1):
            if values[j] > values[j + 1]:
                values[j], values[j + 1] = values[j + 1], values[j]
    return values


def quick_sort(values: list) -> list:
    if not values:
        return values
    center = len(values) // 2
    vcenter = values[center]
    left, right = [], []
    for i, v in enumerate(values):
        if i == center:
            continue
        if v < vcenter:
            left.append(v)
        else:
            right.append(v)
    return quick_sort(left) + [vcenter] + quick_sort(right)


def heap_sort(values: list) -> list:
    heapq.heapify(values)
    result = []
    while values:
        result.append(heapq.heappop(values))
    return result


group = true_north.Group(name='sorting algorithms')


@group.add(name='sorted')
def _():
    with true_north.setup():
        a = random_list()
    sorted(a)


@group.add(name='list.sort')
def _():
    with true_north.setup():
        a = random_list()
    a.sort()


@group.add(name='insert')
def _():
    with true_north.setup():
        a = random_list()
    insert_sort(a)


@group.add(name='select')
def _():
    with true_north.setup():
        a = random_list()
    select_sort(a)


@group.add(name='bubble')
def _():
    with true_north.setup():
        a = random_list()
    bubble_sort(a)


@group.add(name='quick')
def _():
    with true_north.setup():
        a = random_list()
    quick_sort(a)


@group.add(name='heap')
def _():
    with true_north.setup():
        a = random_list()
    heap_sort(a)


if __name__ == '__main__':
    group.run().print()
