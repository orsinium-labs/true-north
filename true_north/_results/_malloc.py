from __future__ import annotations
from collections import Counter
from functools import cached_property

import math
from dataclasses import dataclass
from typing import Iterator, Sequence

from .._colors import DEFAULT_COLORS, Colors
from ._formatters import make_histogram, format_size


CHUNKS = 14


def chunks(items: list[int], count: int) -> Iterator[list[int]]:
    size = math.ceil(len(items) / count)
    for i in range(0, len(items), size):
        yield items[i:i + size]


@dataclass(frozen=True)
class MallocResult:
    """The result of benchmarking memory allocations of a code.
    """
    totals: list[int]           # memory used on each sample
    allocs: list[Counter[str]]  # memory allocations on each sample {file_name: count}

    @cached_property
    def total_allocs(self) -> int:
        """Total memory allocations during the code execution.
        """
        return sum(sum(alloc.values()) for alloc in self.allocs)

    def format(self, colors: Colors = DEFAULT_COLORS) -> str:
        """Generate a human-friendly representation of memory allocations.
        """
        bars: Sequence[float]
        if len(self.totals) < CHUNKS:
            bars = self.totals
        else:
            bars = []
            for chunk in chunks(self.totals, CHUNKS):
                mean = math.fsum(chunk) / len(chunk)
                bars.append(mean)
        return '    {allocs} allocs {used} used {samples} samples  {hist}'.format(
            allocs=colors.magenta(self.total_allocs, group=True, rjust=12),
            used=format_size(max(self.totals), colors=colors, rjust=5),
            samples=colors.magenta(len(self.totals), rjust=9),
            hist=colors.magenta(make_histogram(bars)),
        )