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
def _(r):
    a = random_list()
    for _ in r:
        sorted(a)


@group.add(name='list.sort')
def _(r):
    a = random_list()
    for _ in r:
        a.sort()


@group.add(name='insert')
def _(r):
    a = random_list()
    for _ in r:
        insert_sort(a)


@group.add(name='select')
def _(r):
    a = random_list()
    for _ in r:
        select_sort(a)


@group.add(name='bubble')
def _(r):
    a = random_list()
    for _ in r:
        bubble_sort(a)


@group.add(name='quick')
def _(r):
    a = random_list()
    for _ in r:
        quick_sort(a)


@group.add(name='heap')
def _(r):
    a = random_list()
    for _ in r:
        heap_sort(a)


if __name__ == '__main__':
    group.print()
