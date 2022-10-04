from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

from ._colors import DEFAULT_COLORS, Colors


SCALES = (
    (1.0, 's '),
    (1e-3, 'ms'),
    (1e-6, 'us'),
    (1e-9, 'ns'),
)
TICKS = '▁▂▃▄▅▆▇█'
CHUNKS = len(TICKS) - 1


@dataclass(frozen=True)
class Result:
    name: str
    timings: list[float]
    loops: int

    @property
    def best(self) -> float:
        """The best of all timings (repeats).
        """
        return min(self.timings)

    @cached_property
    def histogram(self) -> str:
        """Histogram of timings (repeats).
        """
        worst = max(self.timings, default=0)
        if worst == 0:
            return TICKS[-1] * len(self.timings)

        histogram = []
        for time in self.timings:
            ratio = time / worst
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
        result = '    {loops:4} loops, best of {repeat}: {best}'.format(
            loops=format_amount(self.loops),
            repeat=len(self.timings),
            best=format_time(self.best, colors=colors),
        )
        if base_time is not None:
            good = self.best < base_time
            if good:
                ratio = round(base_time / self.best, 2)
                ratio_text = f'/{ratio:.02f}'.rjust(8)
                result += f' {colors.green(ratio_text)} faster'
            else:
                ratio = round(self.best / base_time, 2)
                ratio_text = f'x{ratio:.02f}'.rjust(8)
                result += f' {colors.red(ratio_text)} slower'
        else:
            result += ' ' * 16
        result += f' {self.histogram}'
        return result


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
