from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from functools import cached_property

from .._colors import colors
from ._base import BaseResult
from ._formatters import chunks, format_size, make_histogram


@dataclass(frozen=True)
class MallocResult(BaseResult):
    """The result of benchmarking memory allocations of a code.
    """
    totals: list[int]           # memory used on each sample
    allocs: list[Counter[str]]  # memory allocations on each sample {file_name: count}

    @cached_property
    def total_allocs(self) -> int:
        """Total memory allocations during the code execution.
        """
        return sum(sum(alloc.values()) for alloc in self.allocs)

    def format_text(self) -> str:
        """Generate a human-friendly representation of memory allocations.
        """
        return '    {allocs} allocs {used} used {samples} samples'.format(
            allocs=colors.magenta(self.total_allocs, group=True, rjust=12),
            used=format_size(max(self.totals), rjust=5),
            samples=colors.magenta(len(self.totals), rjust=9),
        )

    def format_histogram(self, limit: int = 64, lines: int = 2) -> str:
        bars = []
        for chunk in chunks(self.totals, limit):
            bars.append(math.fsum(chunk) / len(chunk))
        return colors.magenta(make_histogram(bars, lines=lines))
