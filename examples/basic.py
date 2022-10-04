import true_north

group = true_north.Group()


@group.add()
def check_me():
    with true_north.setup():
        a = 1
    a + 2


group.run().print()
