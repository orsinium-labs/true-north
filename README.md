# true-north

Beautiful, powerful, and pythonic benchmarks engine for Python code.

Features:

+ Follows best practices of benchmarking to produce the most reliable results.
+ Detects caching and side-effects.
+ Traces memory usage and allocations (opt-in).
+ Opcodes tracing for reproducble benchmarks (opt-in).
+ 100% type safe.
+ Zero dependency.
+ Highly configurable.
+ Nice and colorful output.
+ Ships with CLI to discover and run all benchmarks.
+ A friendly API to write your own logic on top of benchmarks.

```text
sorting algorithms
  list.sort
    possible side-effect detected: slowest iteration x21 slower than fastest
    5k   loops, best of 5:  43.579 us ±  12.681 us                 ████▇
              11 ops, 3961 ns/op
  sorted
    5k   loops, best of 5:  43.911 us ±   3.697 us    x1.01 slower █████
              11 ops, 3991 ns/op
  insert_sort
    2    loops, best of 5: 100.662 ms ± 111.725 us x2309.85 slower █████
      11_683_767 ops,    8 ns/op
```

## Installation

```bash
python3 -m pip install true-north
```

## Usage

```python
import true_north

group = true_north.Group()

@group.add
def math_sorted(r):
    val = [1, 2, 3] * 300
    # timer start before entering the loop
    # and stops when leaving it
    for _ in r:
        sorted(val)

# run and print all benchmarks in the group
if __name__ == '__main__':
    group.print()
```

See [examples](./examples/) for more examples and [true-north.orsinium.dev](https://true-north.orsinium.dev/) for chad documentation.
