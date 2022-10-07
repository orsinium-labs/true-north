import true_north


group = true_north.Group(name='Group')


@group.add(name='__init__ without name')
def _(r):
    for _ in r:
        true_north.Group()


@group.add(name='__init__ with name')
def _(r):
    for _ in r:
        true_north.Group(name='oh hi mark')


def noop(r=None):
    pass


@group.add(name='add()')
def _(r):
    group = true_north.Group()
    for _ in r:
        group.add()(noop)


@group.add(name='add')
def _(r):
    group = true_north.Group()
    for _ in r:
        group.add(noop)


if __name__ == '__main__':
    group.print()
