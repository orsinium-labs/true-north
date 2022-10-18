from __future__ import annotations

import gc
from dataclasses import dataclass
from typing import Callable, Iterable

from ._colors import colors
from ._config import DEFAULT_CONFIG, Config
from ._loopers import (
    EachLooper, MemoryLooper, OpcodeLooper, Timer, TotalLooper,
)
from ._results import MallocResult, OpcodesResult, TimingResult


Func = Callable[[Iterable[int]], None]


@dataclass(frozen=True)
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

    def print(
        self,
        config: Config = DEFAULT_CONFIG,
        base_time: float | None = None,
    ) -> TimingResult:
        print_args: dict = dict(
            stream=config.stream,
            histogram_lines=config.histogram_lines,
        )
        print(f'  {colors.magenta(self.name)}', file=config.stream)
        tresult = self.check_timing()
        tresult._base_time = base_time
        tresult.print(**print_args)
        if config.allocations or config.opcodes:
            oresult = self.check_opcodes(best=tresult.best)
            oresult.print(**print_args)
        if config.allocations:
            mresult = self.check_mallocs(lines=oresult.lines)
            mresult.print(**print_args)
        return tresult

    def check_timing(self) -> TimingResult:
        """Run benchmarks for the check.
        """
        # to detect caching, we should individually record
        # the very first run
        each_timings = self._run_each_loop(2)
        total_timings = []
        loops = self.loops
        repeats = self.repeats
        if loops is None:
            loops, raw_timing = self._autorange()
            total_timings.append(raw_timing)
            repeats -= 1
        if loops > 2:
            each_timings.extend(self._run_each_loop(loops - 2))

        for _ in range(repeats):
            total_timings.append(self._run_total_loop(loops))
        assert len(total_timings) == self.repeats
        return TimingResult(
            total_timings=[dt / loops for dt in total_timings],
            each_timings=each_timings,
        )

    def check_opcodes(self, loops: int = 1, best: float = 0) -> OpcodesResult:
        """Run the benchmark and count executed opcodes.
        """
        looper = OpcodeLooper(loops=loops)
        self._run(looper)
        return OpcodesResult(
            opcodes=looper.opcodes,
            lines=looper.lines,
            timings=looper.timings,
            best=best,
        )

    def check_mallocs(self, lines: int, loops: int = 1) -> MallocResult:
        """Run the benchmark and trace memory allocations.
        """
        period = max(1, round(lines / 500))
        looper = MemoryLooper(period=period, loops=loops)
        self.func(looper)
        return MallocResult(
            totals=looper.totals,
            allocs=looper.allocs,
        )

    # Private methods

    def _run_total_loop(self, loops: int = 1) -> float:
        looper = TotalLooper(loops=loops, timer=self.timer)
        self._run(looper)
        return looper.stop - looper.start

    def _run_each_loop(self, loops: int) -> list[float]:
        looper = EachLooper(loops=loops, timer=self.timer, timings=[])
        self._run(looper)
        assert len(looper.timings) == loops
        return looper.timings

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
                time_taken = self._run_total_loop(number)
                if time_taken >= self.min_time:
                    return number, time_taken
            i *= 10
