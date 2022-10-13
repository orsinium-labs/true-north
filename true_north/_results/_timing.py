from __future__ import annotations

import math
from dataclasses import dataclass
from functools import cached_property

from .._colors import colors
from ._formatters import format_amount, format_time, make_histogram


@dataclass(frozen=True)
class TimingResult:
    """The result of benchmarking a code execution time.
    """
    total_timings: list[float]  # mean time per loop for each repeat
    each_timings: list[float]   # execution time of each loop in a single repeat

    @property
    def best(self) -> float:
        """The best of all timings (repeats).
        """
        return min(self.total_timings)

    @cached_property
    def histogram(self) -> str:
        """Histogram of timings (repeats).
        """
        return make_histogram(self.total_timings)

    @cached_property
    def stdev(self) -> float:
        """Standard deviation of loops in a single repeat.

        If there is only one loop in each repeat, use all repeats instead.
        """
        ts = self.each_timings
        if len(ts) == 1:
            ts = self.total_timings
        mean = math.fsum(ts) / len(ts)
        return (math.fsum((t - mean) ** 2 for t in ts) / len(ts)) ** 0.5

    def format(
        self,
        base_time: float | None = None,
    ) -> str:
        """Represent the timing result as a human-friendly text.
        """
        result = '    {loops:4} loops, best of {repeat}: {best} ± {stdev}'.format(
            loops=format_amount(len(self.each_timings)),
            repeat=len(self.total_timings),
            best=format_time(self.best),
            stdev=format_time(self.stdev),
        )
        if base_time is not None:
            good = self.best < base_time
            if good:
                ratio = round(base_time / self.best, 2)
                ratio_text = f'/{ratio:.02f}'
                result += f' {colors.green(ratio_text, rjust=8)} faster'
            else:
                ratio = round(self.best / base_time, 2)
                ratio_text = f'x{ratio:.02f}'
                result += f' {colors.red(ratio_text, rjust=8)} slower'
        else:
            result += ' ' * 16
        result += f' {self.histogram}'
        return result

    def format_warning(self) -> str:
        first = self.each_timings[0]
        second = self.each_timings[1]
        if second != 0 and first > 1e-6:
            ratio = first / second
            if ratio > 2:
                warn = 'possible caching detected'
                descr = f'first iteration x{ratio:.0f} slower than second'
                return f'    {colors.yellow(warn)}: {descr}'

        fastest = min(self.each_timings)
        if fastest == 0:
            warn = 'the fastest time is 0'
            descr = 'the timer function is not detailed enough'
            return f'    {colors.yellow(warn)}: {descr}'

        if fastest < 0:
            warn = 'the fastest time is negative'
            descr = 'the timer function is not monotonic'
            return f'    {colors.yellow(warn)}: {descr}'

        slowest = max(self.each_timings)
        if slowest > 1e-6:
            ratio = slowest / fastest
            if ratio > 4:
                warn = 'possible side-effect detected'
                descr = f'slowest iteration x{ratio:.0f} slower than fastest'
                return f'    {colors.yellow(warn)}: {descr}'

        return ''
