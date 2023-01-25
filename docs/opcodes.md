# Trace opcodes

The library can track the number of [opcodes](https://docs.python.org/3/library/dis.html) executed by the benchmark function. The idea is similar to how [benchee](https://github.com/bencheeorg/benchee) [counts reductions](https://github.com/bencheeorg/benchee#measuring-reductions) (function calls) for Erlang code. The difference between measuring execution time and executed opcodes is that the latter is reproducible. There are a few catches, though:

1. Different version of Python produce different number of opcodes. Always run benchmarks on the same Python interpreter.
1. Tracing opcodes requires true-north to register multiple tracing hooks, which slows down the code execution. It won't affect the timing benchmarks, but it will take more time to run the suite.
1. More opcodes doesn't mean slower code. Different opcodes take different time to run. In particular, calling a C function (like `sorted`) is just one opcode. However, if you compare two pure Python functions that don't use call anything heavy, opcodes will roughly correlate with the execution time.

To track opcodes, run CLI with `--opcodes` or call `Group.print` with `Config(opcodes=True)`.

## Reading output

```text
10_031 ops  18 ns/op  2010 lines
```

+ `10_031 ops`: a single loop executed 10031 opcodes. Read the section above to learn more about opcodes.
+ `18 ns/op`: execution of each opcode took on average 18 nanoseconds.
+ `2010 lines`: when tracing opcodes, 2010 lines of code were executed. If a line is executed twice, it is counted twice. See [lnotab_notes.txt](https://github.com/python/cpython/blob/main/Objects/lnotab_notes.txt) on what Python considers a line of code. You shouldn't optimize your code for fewer lines (or opcodes) but this number can reveal to you unexpected randomness in your code.
