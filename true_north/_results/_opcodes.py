

from __future__ import annotations

from dataclasses import dataclass
import math

from .._colors import colors
from ._formatters import chunks, make_histogram


@dataclass(frozen=True)
class OpcodesResult:
    """The result of benchmarking opcodes executed by a code.
    """
    opcodes: int    # number of opcodes executed
    lines: int      # number of lines executed (see lnotab_notes.txt in CPython)
    timings: list[float]
    best: float     # the best execution time, used to calculate ns/op.

    def format(self) -> str:
        """Generate a human-friendly representation of opcodes.
        """
        bars = []
        for chunk in chunks(self.timings, 10):
            bars.append(math.fsum(chunk) / len(chunk))
        return '    {opcodes} ops {ns_op} ns/op {lines} lines  {hist}'.format(
            opcodes=colors.cyan(self.opcodes, rjust=12, group=True),
            ns_op=colors.cyan(int(self.best * 1e9 // self.opcodes), rjust=8),
            lines=colors.cyan(self.lines, rjust=12, group=True),
            hist=colors.cyan(make_histogram(bars)),
        )
