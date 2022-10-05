# true-north

Beautiful and pythonic benchmarks engine for Python code.

Features:

+ Follows best practices of benchmarking to produce the most reliable results.
+ Detects caching and side-effects.
+ Opcodes tracing for reproducble benchmarks.
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
if __name__ == '__main__':
    group.print()
```

See [examples](./examples/) for more examples.

## Tracing opcodes

If you run CLI with `--opcodes` or call `Group.print` with `opcodes=True`, the output will also include the number of [opcodes](https://docs.python.org/3/library/dis.html) executed by the benchmark function. The idea is similar to how [benchee](https://github.com/bencheeorg/benchee) [counts reductions](https://github.com/bencheeorg/benchee#measuring-reductions) (function calls) for Erlang code. The difference between measuring execution time and executed opcodes is that the latter is reproducible. There are a few catches, though:

1. Different version of Python produce different number of opcodes. Always run benchmarks on the same Python interpreter.
1. Tracing opcodes requires true-north to register multiple tracing hooks, which slows down the code execution. It won't affect the timing benchmarks, but it will take more time to run the suite.
1. More opcodes doesn't mean slower code. Different opcodes take different time to run. In particular, calling a C function (like `sorted`) is just one opcode. However, if you compare two pure Python functions that don't use call anything heavy, opcodes will roughly correlate with the execution time.

![output example with opcodes](./opcodes.png)
