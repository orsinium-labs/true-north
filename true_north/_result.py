from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

SCALES = (
    (1.0, 's'),
    (1e-3, 'ms'),
    (1e-6, 'us'),
    (1e-9, 'ns'),
)
TICKS = '▁▂▃▄▅▆▇█'
CHUNKS = 6
PRECISION = 3


@dataclass(frozen=True)
class Result:
    name: str
    timings: list[float]
    loops: int

    @property
    def best(self) -> float:
        return min(self.timings)

    @cached_property
    def histogram(self) -> str:
        best = 0
        worst = max(self.timings)
        diff = worst - best

        if diff == 0:
            return TICKS[-1] * CHUNKS

        histogram = []
        for time in self.timings:
            ratio = (time - best) / diff
            index = int(round(ratio * CHUNKS))
            histogram.append(TICKS[index])
        return ''.join(histogram)

    @cached_property
    def text(self) -> str:
        return '    {loops} loops, best of {repeat}: {best} {hist}'.format(
            loops=format_amount(self.loops),
            repeat=len(self.timings),
            best=format_time(self.best),
            hist=self.histogram,
        )


def format_time(dt: float) -> str:
    for scale, unit in SCALES:
        if dt >= scale:
            break
    value = round(dt / scale, PRECISION)
    return f'{value} {unit}'


def format_amount(number: float, k: int = 0) -> str:
    if number < 1000:
        suffix = 'k' * k
        return f'{number:.0f}{suffix}'
    return format_amount(number / 1000, k + 1)
