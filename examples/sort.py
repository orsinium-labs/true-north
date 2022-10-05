from functools import partial
import heapq
from random import randint, seed

import true_north

seed(13)


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


@group.add(name='list.sort')
def _(r):
    base_list = random_list()
    for _ in r:
        a = base_list.copy()
        a.sort()


def bench(func, r):
    base_list = random_list()
    for _ in r:
        a = base_list.copy()
        func(a)


# true-north doesn't do any static analysis,
# so you can define benchmarks dynamically.
FUNCS = (sorted, insert_sort, select_sort, bubble_sort, quick_sort, heap_sort)
for func in FUNCS:
    group.add(name=func.__name__)(partial(bench, func))


if __name__ == '__main__':
    group.print()
