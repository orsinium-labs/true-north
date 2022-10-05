from __future__ import annotations

from dataclasses import dataclass
import gc
from typing import Callable, Iterable

from ._loopers import TotalLooper, Timer, EachLooper, OpcodeLooper
from ._result import Result


Func = Callable[[Iterable[int]], None]


@dataclass
class Check:
    """A single benchmark.

    Don't instancinate directly, use `Group.add` decorator instead.
    """
    name: str
    func: Func
    loops: int | None
    repeats: int
    min_time: float
    timer: Timer

    def run(self) -> Result:
        """Run benchmarks for the check.
        """
        # to detect caching, we should individually record
        # the very first run
        each_timings = self._run_each_loop(2)
        total_timings = []
        loops = self.loops
        if loops is None:
            loops, raw_timing = self._autorange()
            total_timings.append(raw_timing)
        if loops > 2:
            each_timings.extend(self._run_each_loop(loops - 2))

        for _ in range(self.repeats - 1):
            total_timings.append(self.run_once(loops))
        assert len(total_timings) == self.repeats
        return Result(
            name=self.name,
            total_timings=[dt / loops for dt in total_timings],
            each_timings=each_timings,
            loops=loops,
        )

    def run_once(self, loops: int = 1) -> float:
        looper = TotalLooper(loops=loops, timer=self.timer)
        self._run(looper)
        return looper.stop - looper.start

    def _run_each_loop(self, loops: int) -> list[float]:
        looper = EachLooper(loops=loops, timer=self.timer, timings=[])
        self._run(looper)
        assert len(looper.timings) == loops
        return looper.timings

    def count_opcodes(self, loops: int = 1) -> int:
        """Run the benchmark and count executed opcodes.
        """
        looper = OpcodeLooper(loops=loops)
        self._run(looper)
        return looper.count

    def _run(self, looper: Iterable[int]) -> None:
        gc_was_enabled = gc.isenabled()
        gc.disable()
        try:
            self.func(looper)
        finally:
            if gc_was_enabled:
                gc.enable()

    def _autorange(self) -> tuple[int, float]:
        """Return the number of loops so that total time is at least min_time.

        Calls the timeit method with increasing numbers from the sequence
        1, 2, 5, 10, 20, 50, ... until the time taken is at least 0.2
        second.
        """
        i = 1
        while True:
            for j in 1, 2, 5:
                number = i * j
                time_taken = self.run_once(number)
                if time_taken >= self.min_time:
                    return number, time_taken
            i *= 10
