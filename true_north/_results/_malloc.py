from __future__ import annotations

import math
from collections import Counter

from .._colors import colors
from ._base import BaseResult
from ._formatters import chunks, format_size, make_histogram


class MallocResult(BaseResult):
    """The result of benchmarking memory allocations of a code.
    """
    _totals: list[int]
    _allocs: list[Counter[str]]

    def __init__(self, totals: list[int], allocs: list[Counter[str]]) -> None:
        self._totals = totals
        self._allocs = allocs

    @property
    def totals(self) -> list[int]:
        """Total memory used by the code on each sample.
        """
        return self._totals

    @property
    def allocs(self) -> list[Counter[str]]:
        """Memory allocations in each file for each sample.

        Each item of the list is a Counter for a single sample.
        The Counter holds the number of allocations in each file.
        """
        return self._allocs

    @property
    def total_allocs(self) -> int:
        """Total memory allocations during the code execution.
        """
        return sum(sum(alloc.values()) for alloc in self._allocs)

    def format_text(self) -> str:
        """Generate a human-friendly representation of memory allocations.
        """
        return '    {allocs} allocs {used} used {samples} samples'.format(
            allocs=colors.magenta(self.total_allocs, group=True, rjust=12),
            used=format_size(max(self._totals), rjust=5),
            samples=colors.magenta(len(self._totals), rjust=9),
        )

    def format_histogram(self, limit: int = 64, lines: int = 2) -> str:
        bars = []
        for chunk in chunks(self._totals, limit):
            bars.append(math.fsum(chunk) / len(chunk))
        return colors.magenta(make_histogram(bars, lines=lines))
