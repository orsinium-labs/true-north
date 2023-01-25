# Trace memory allocations

The library can trace [memory allocations](https://www.cs.uah.edu/~rcoleman/Common/C_Reference/MemoryAlloc.html) but doesn't do it by default because it is expensive (in terms of execution time). And to keep the benchmark execution time reasonable when tracing memory, true-north will collect the sample only after some operations, not all of them. So, the real numbers of allocations and usage might be higher.

To track memory allocations, run CLI with `--mallocs` or call `Group.print` with `Config(mallocs=True)`.

## Reading output

```text
1438 allocs  139 KiB used  501 samples
```

+ `1438 allocs`: how many memory allocations happened during one loop.
+ `139 KiB used`: the size of the biggest memory sample collected. The same as for allocations, the real number might be higher.
+ `501 samples`: how many memory samples were collected. By default true-north tries to collect about 500 samples. It does so by tracking during opcode pass how many lines of code were executed, and then divinding this number by 500 to get how often sampling should be trigered.
