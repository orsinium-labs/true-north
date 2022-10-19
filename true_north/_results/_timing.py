from __future__ import annotations

import math

from .._colors import colors
from ._base import BaseResult
from ._formatters import format_amount, format_time, make_histogram


class TimingResult(BaseResult):
    """The result of benchmarking a code execution time.
    """
    __slots__ = ('_total_timings', '_each_timings', '_base_time')

    _total_timings: list[float]
    _each_timings: list[float]
    _base_time: float | None

    def __init__(
        self,
        total_timings: list[float],
        each_timings: list[float],
    ) -> None:
        self._total_timings = total_timings
        self._each_timings = each_timings
        self._base_time = None

    @property
    def total_timings(self) -> list[float]:
        """Average time per loop for each repeat (bechmarking function call).
        """
        return self._total_timings

    @property
    def loop_timings(self) -> list[float]:
        """Execution time of each loop in a single repeat (bechmarking function call).
        """
        return self._each_timings

    @property
    def best(self) -> float:
        """The best of all total timings (repeats).
        """
        return min(self._total_timings)

    @property
    def stdev(self) -> float:
        """Standard deviation of loops in a single repeat.

        If there is only one loop in each repeat, use all repeats instead.
        """
        ts = self._each_timings
        if len(ts) == 1:
            ts = self._total_timings
        mean = math.fsum(ts) / len(ts)
        return (math.fsum((t - mean) ** 2 for t in ts) / len(ts)) ** 0.5

    def format_histogram(self, limit: int = 64, lines: int = 2) -> str:
        """Histogram of timings (repeats).
        """
        assert len(self._total_timings) <= limit
        return make_histogram(self._total_timings, lines=lines)

    def format_text(self) -> str:
        """Represent the timing result as a human-friendly text.
        """
        result = '{loops:4} loops, best of {repeat}: {best} ± {stdev}'.format(
            loops=format_amount(len(self._each_timings)),
            repeat=len(self._total_timings),
            best=format_time(self.best),
            stdev=format_time(self.stdev),
        )
        if self._base_time is not None:
            good = self.best < self._base_time
            if good:
                ratio = round(self._base_time / self.best, 2)
                ratio_text = f'/{ratio:.02f}'
                result += f' {colors.green(ratio_text, rjust=8)} faster'
            else:
                ratio = round(self.best / self._base_time, 2)
                ratio_text = f'x{ratio:.02f}'
                result += f' {colors.red(ratio_text, rjust=8)} slower'
        return result

    def format_warnings(self) -> list[str]:
        result = []

        first = self._each_timings[0]
        second = self._each_timings[1]
        if second != 0 and first > 1e-6:
            ratio = first / second
            if ratio > 2:
                warn = 'possible caching detected'
                descr = f'first iteration x{ratio:.0f} slower than second'
                result.append(f'{colors.yellow(warn)}: {descr}')

        fastest = min(self._each_timings)
        if fastest == 0:
            warn = 'the fastest time is 0'
            descr = 'the timer function is not detailed enough'
            result.append(f'{colors.yellow(warn)}: {descr}')
            return result

        if fastest < 0:
            warn = 'the fastest time is negative'
            descr = 'the timer function is not monotonic'
            result.append(f'{colors.yellow(warn)}: {descr}')

        slowest = max(self._each_timings)
        if slowest > 1e-6:
            ratio = slowest / fastest
            if ratio > 4:
                warn = 'possible side-effect detected'
                descr = f'slowest iteration x{ratio:.0f} slower than fastest'
                result.append(f'{colors.yellow(warn)}: {descr}')

        return result
