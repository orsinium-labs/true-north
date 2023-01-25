# Benchmark execution time

...

## Reading output

Let's take the following benchmark output as an example:

```text
1k loops, best of 5: 240.487 us ± 4.723 us x5.68 slower
```

+ `1k loops`: each time the benchmarking function was called, the loop in it was executed 1000 times. So, if you defined the function as `def heap_sort(r)`, the `r` value is an iterable object with 1000 items. By default, this value is adjusted to finish benchmarking in a reasonable time, but you can specify it explicitly using `loops` argument.
+ `best of 5`: the benchmarking function was called 5 times, and the resulting execution time shown on the right is the best result out of these 5 calls. We do that to minimize how CPU usage by other programs on your machine affects the result. It's 5 by default, but you can change it with `repeats` argument.
+ `240.487 us`: the average execution time of a sinlge loop iteration is about 240 microseconds (ms is 1e−6 of a second).
+ `± 4.723 us`: the standard deviation of each loop iteration is 4.723 microseconds. It is a good value. If it gets close to the average execution time, though, the results aren't reliable. I there was only one loop, the standard deviation will be calculated for all repeats instead.
+ `x5.68 slower`: the average execution time is 5.7 times slower that that of the base benchmark. The base benchmark is the first one in the group. It's always a good idea to have a base benchmark you compare other results to. For example, if you compare your library against other libraries, put the benchmark for your library first to see how you're doing compared to others.
+ `█████`: a histogram where each block represents one repeat (benchmarking function call). The minimum value is 0 and the maximum value is the slowest repeat. If all blocks of the same size, results are good. If you see fluctation in their size, results aren't so reliable, and something affects benchmarks too much. To fix it, you can try to explicitly set a higher value for `loops` argument.
