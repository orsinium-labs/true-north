from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Callable, Iterable, Iterator
from ._result import Result

Func = Callable[[Iterable[int]], None]
Timer = Callable[..., float]


@dataclass
class Looper:
    loops: int
    start: float = 0
    stop: float = 0
    timer: Callable[..., float] = perf_counter

    def __iter__(self) -> Iterator[int]:
        self.start = self.timer()
        for i in range(self.loops):
            yield i
        self.stop = self.timer()


@dataclass
class Check:
    name: str | None
    func: Func
    loops: int | None
    repeats: int

    def run(self) -> Result:
        """Run benchmarks for the check.
        """
        loops = self.loops
        if loops is None:
            loops = self._autorange()
        raw_timings = []
        for _ in range(self.repeats):
            raw_timings.append(self.run_once(loops))
        assert len(raw_timings) == self.repeats
        return Result(
            name=self.name or self.func.__name__,
            timings=[dt / loops for dt in raw_timings],
            loops=loops,
        )

    def run_once(self, loops: int = 1) -> float:
        looper = Looper(loops=loops)
        self.func(looper)
        return looper.stop - looper.start

    def _autorange(self) -> int:
        """Return the number of loops and time taken so that total time >= 0.2.

        Calls the timeit method with increasing numbers from the sequence
        1, 2, 5, 10, 20, 50, ... until the time taken is at least 0.2
        second.  Returns (number, time_taken).

        If *callback* is given and is not None, it will be called after
        each trial with two arguments: ``callback(number, time_taken)``.
        """
        i = 1
        while True:
            for j in 1, 2, 5:
                number = i * j
                time_taken = self.run_once(number)
                if time_taken >= 0.2:
                    return number
            i *= 10
