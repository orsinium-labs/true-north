# true-north

Beautiful and pythonic benchmarks engine for Python code.

Features:

+ Follows best practices of benchmarking to produce the most reliable results.
+ Detects caching and side-effects.
+ 100% type safe.
+ Zero dependency.
+ Highly configurable.
+ Nice and colorful output.
+ Ships with CLI to discover and run all benchmarks.

![output example](./example.png)

## Installation

```bash
pytohn3 -m pip install true-north
```

## Usage

```python
import true_north

group = true_north.Group()

@group.add()
def math_sorted(r):
    val = [1, 2, 3] * 300
    # timer start before entering the loop
    # and stops when leaving it
    for _ in r:
        sorted(val)

# run and print all benchmarks in the group
group.print()
```

See [examples](./examples/) for more examples.
