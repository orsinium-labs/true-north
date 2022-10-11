from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Iterator, Sequence

from .._colors import DEFAULT_COLORS, Colors
from ._formatters import make_histogram, format_size


def chunks(items: list[int], count: int) -> Iterator[list[int]]:
    size = math.ceil(len(items) / count)
    for i in range(0, len(items), size):
        yield items[i:i + size]


@dataclass
class MallocResult:
    totals: list[int] = field(default_factory=list)

    def format(self, colors: Colors = DEFAULT_COLORS) -> str:
        """Generate a human-friendly representation of memory allocations.
        """
        samples = colors.magenta(len(self.totals), rjust=12, group=True)
        peak = format_size(max(self.totals), colors=colors)
        bars: Sequence[float]
        if len(self.totals) < 20:
            bars = self.totals
        else:
            bars = []
            for chunk in chunks(self.totals, 20):
                mean = math.fsum(chunk) / len(chunk)
                bars.append(mean)
        hist = make_histogram(bars)
        return f'    {samples} samples, {peak} peak {hist}'
