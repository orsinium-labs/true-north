

from __future__ import annotations

import math
from dataclasses import dataclass

from .._colors import colors
from ._base import BaseResult
from ._formatters import chunks, make_histogram


@dataclass(frozen=True)
class OpcodesResult(BaseResult):
    """The result of benchmarking opcodes executed by a code.
    """
    opcodes: int    # number of opcodes executed
    lines: int      # number of lines executed (see lnotab_notes.txt in CPython)
    timings: list[float]
    best: float     # the best execution time, used to calculate ns/op.

    def format_text(self) -> str:
        """Generate a human-friendly representation of opcodes.
        """
        return '    {opcodes} ops {ns_op} ns/op {lines} lines'.format(
            opcodes=colors.cyan(self.opcodes, rjust=12, group=True),
            ns_op=colors.cyan(int(self.best * 1e9 // self.opcodes), rjust=8),
            lines=colors.cyan(self.lines, rjust=12, group=True),
        )

    def format_histogram(self, limit: int = 64) -> str:
        bars = []
        for chunk in chunks(self.timings, limit):
            bars.append(math.fsum(chunk) / len(chunk))
        return colors.cyan(make_histogram(bars))
