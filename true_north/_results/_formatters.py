from __future__ import annotations

from typing import Sequence

from .._colors import Colors


SCALES = (
    (1.0, 's '),
    (1e-3, 'ms'),
    (1e-6, 'us'),
    (1e-9, 'ns'),
)
TICKS = '▁▂▃▄▅▆▇█'
CHUNKS = len(TICKS) - 1


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


def format_size(size: float, colors: Colors, rjust: int) -> str:
    for unit in ('B  ', 'KiB', 'MiB', 'GiB', 'TiB'):
        if abs(size) < 100 and unit != 'B':
            size_text = colors.magenta(size, rjust=rjust, precision=1)
            return f'{size_text} {colors.color_unit(unit)}'
        if abs(size) < 10 * 1024 or unit == 'TiB':
            # 4 or 5 digits (xxxx UNIT)
            size_text = colors.magenta(int(size), rjust=rjust)
            return f'{size_text} {colors.color_unit(unit)}'
        size /= 1024
    raise RuntimeError


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
