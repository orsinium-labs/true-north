import true_north

# Group is a collection of benchmarks.
# If you don't specify `name`, file name and line number will be used instead.
group = true_north.Group()


@group.add()
def check_me():
    with true_north.setup():
        a = 1
    a + 2


if __name__ == '__main__':
    group.run().print()
