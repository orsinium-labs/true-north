from __future__ import annotations

import gc
from dataclasses import dataclass
import sys
from typing import Callable, Iterable, TextIO

from ._loopers import EachLooper, OpcodeLooper, Timer, TotalLooper, MemoryLooper
from ._result import Result
from ._colors import DEFAULT_COLORS, Colors


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

    def print(
        self,
        stream: TextIO = sys.stdout,
        colors: Colors = DEFAULT_COLORS,
        opcodes: bool = False,
        allocations: bool = False,
        base_time: float | None = None,
    ) -> Result:
        print(f'  {colors.magenta(self.name)}', file=stream)
        result = self.run()
        warning = result.format_warning(colors=colors)
        if warning:
            print(warning, file=stream)
        print(result.format_timing(colors=colors, base_time=base_time), file=stream)
        if opcodes:
            opcode_looper = self._count_opcodes()
            result.opcodes = opcode_looper.opcodes
            result.lines = opcode_looper.lines
            print(result.format_opcodes(), file=stream)
        if allocations:
            result.allocations = self._count_allocations(lines=result.lines)
            print(result.format_allocations(), file=stream)
        return result

    def run(self) -> Result:
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

    def _count_opcodes(self, loops: int = 1) -> OpcodeLooper:
        """Run the benchmark and count executed opcodes.
        """
        looper = OpcodeLooper(loops=loops)
        self._run(looper)
        return looper

    def _count_allocations(self, lines: int) -> list[int]:
        period = max(1, round(lines / 4000))
        looper = MemoryLooper(
            loops=1,
            snapshots=[],
            period=period,
        )
        self._run(looper)
        return looper.snapshots

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
