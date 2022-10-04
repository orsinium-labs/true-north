from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from ._colors import Colors, DEFAULT_COLORS

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

    def get_text(
        self,
        colors: Colors = DEFAULT_COLORS,
        base_time: float | None = None,
    ) -> str:
        """Represent the result as a line of text.
        """
        result = '    {loops:4} loops, best of {repeat}: {best:>12}'.format(
            loops=format_amount(self.loops),
            repeat=len(self.timings),
            best=format_time(self.best),
        )
        if base_time is not None:
            ratio = round(self.best / base_time, 2)
            coloring = colors.green if ratio <= 1 else colors.red
            ratio_text = f'x{ratio}'.rjust(8)
            result += f' {coloring(ratio_text)}'
        else:
            result += ' ' * 9
        result += f' {self.histogram}'
        return result


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
