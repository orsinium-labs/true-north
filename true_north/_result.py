from __future__ import annotations

import math
from dataclasses import dataclass, field
from functools import cached_property
from typing import Iterator, Sequence

from ._colors import DEFAULT_COLORS, Colors


SCALES = (
    (1.0, 's '),
    (1e-3, 'ms'),
    (1e-6, 'us'),
    (1e-9, 'ns'),
)
TICKS = '▁▂▃▄▅▆▇█'
CHUNKS = len(TICKS) - 1


@dataclass
class Result:
    name: str
    total_timings: list[float]
    each_timings: list[float]
    loops: int

    # not calculated by default
    opcodes: int = 0
    lines: int = 0
    allocations: list[int] = field(default_factory=list)

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

    def format_timing(
        self,
        colors: Colors = DEFAULT_COLORS,
        base_time: float | None = None,
    ) -> str:
        """Represent the result as a line of text.
        """
        result = '    {loops:4} loops, best of {repeat}: {best}'.format(
            loops=format_amount(self.loops),
            repeat=len(self.total_timings),
            best=format_time(self.best, colors=colors),
        )
        result += f' ± {format_time(self.stdev, colors=colors)}'
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

    def format_warning(self, colors: Colors = DEFAULT_COLORS) -> str:
        first = self.each_timings[0]
        second = self.each_timings[1]
        if second != 0 and first > 1e-6:
            ratio = first / second
            if ratio > 2:
                warn = 'possible caching detected'
                descr = f'first iteration x{ratio:.0f} slower than second'
                return f'{colors.yellow(warn)}: {descr}'

        fastest = min(self.each_timings)
        if fastest == 0:
            warn = 'the fastest time is 0'
            descr = 'the timer function is not detailed enough'
            return f'{colors.yellow(warn)}: {descr}'

        if fastest < 0:
            warn = 'the fastest time is negative'
            descr = 'the timer function is not monotonic'
            return f'{colors.yellow(warn)}: {descr}'

        slowest = max(self.each_timings)
        if slowest > 1e-6:
            ratio = slowest / fastest
            if ratio > 4:
                warn = 'possible side-effect detected'
                descr = f'slowest iteration x{ratio:.0f} slower than fastest'
                return f'{colors.yellow(warn)}: {descr}'

        return ''

    def format_opcodes(self, colors: Colors = DEFAULT_COLORS) -> str:
        """Generate a human-friendly representation of opcodes.
        """
        opcodes = colors.cyan(self.opcodes, rjust=12, group=True)
        ns_op = colors.cyan(int(self.best * 1e9 // self.opcodes), rjust=9)
        lines = colors.cyan(self.lines, rjust=12, group=True)
        return f'    {opcodes} ops, {ns_op} ns/op {lines} lines'

    def format_allocations(self, colors: Colors = DEFAULT_COLORS) -> str:
        """Generate a human-friendly representation of memory allocations.
        """
        samples = colors.magenta(len(self.allocations), rjust=12, group=True)
        peak = format_size(max(self.allocations), colors=colors)
        bars: Sequence[float]
        if len(self.allocations) < 20:
            bars = self.allocations
        else:
            bars = []
            for chunk in chunks(self.allocations, 20):
                mean = math.fsum(chunk) / len(chunk)
                bars.append(mean)
        hist = make_histogram(bars)
        return f'    {samples} samples, {peak} peak {hist}'


def format_time(dt: float, colors: Colors) -> str:
    for scale, unit in SCALES:
        if dt >= scale:
            break
    value = f'{dt/scale:3.03f}'.rjust(7)
    return f'{value} {colors.color_unit(unit)}'


def format_amount(number: float, k: int = 0) -> str:
    if number < 1000:
        suffix = 'k' * k
        return f'{number:.0f}{suffix}'
    return format_amount(number / 1000, k + 1)


def format_size(size: float, colors: Colors) -> str:
    for unit in ('B  ', 'KiB', 'MiB', 'GiB', 'TiB'):
        if abs(size) < 100 and unit != 'B':
            size_text = colors.magenta(size, rjust=5, precision=1)
            return f'{size_text} {colors.color_unit(unit)}'
        if abs(size) < 10 * 1024 or unit == 'TiB':
            # 4 or 5 digits (xxxx UNIT)
            size_text = colors.magenta(int(size), rjust=5)
            return f'{size_text} {colors.color_unit(unit)}'
        size /= 1024
    raise RuntimeError


def chunks(items: list[int], count: int) -> Iterator[list[int]]:
    size = math.ceil(len(items) / count)
    for i in range(0, len(items), size):
        yield items[i:i + size]


def make_histogram(items: Sequence[float]):
    worst = max(items, default=0)
    if worst == 0:
        return TICKS[-1] * len(items)

    histogram = []
    for item in items:
        ratio = item / worst
        index = int(round(ratio * CHUNKS))
        histogram.append(TICKS[index])
    return ''.join(histogram)
