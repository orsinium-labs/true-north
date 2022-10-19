

from __future__ import annotations

import math

from .._colors import colors
from ._base import BaseResult
from ._formatters import chunks, make_histogram


class OpcodesResult(BaseResult):
    """The result of benchmarking opcodes executed by a code.
    """
    __slots__ = ('_opcodes', '_lines', '_timings', '_best')

    _opcodes: int
    _lines: int
    _timings: list[float]
    _best: float

    def __init__(
        self,
        opcodes: int,
        lines: int,
        timings: list[float],
        best: float,
    ) -> None:
        self._opcodes = opcodes
        self._lines = lines
        self._timings = timings
        self._best = best

    @property
    def opcodes_count(self) -> int:
        """Number of opcodes executed.
        """
        return self._opcodes

    @property
    def lines(self) -> int:
        """Number of lines of code executed.

        See lnotab_notes.txt in CPython to learn more what is considered line.
        """
        return self._lines

    @property
    def timings(self) -> list[float]:
        """The time when each opcode was executed.
        """
        return self._timings

    @property
    def durations(self) -> list[float]:
        """How long it took to execute each opcode.
        """
        diffs = []
        for left, right in zip(self._timings, self._timings[1:]):
            diffs.append(right - left)
        return diffs

    def format_text(self) -> str:
        """Generate a human-friendly representation of opcodes.
        """
        return '    {opcodes} ops {ns_op} ns/op {lines} lines'.format(
            opcodes=colors.cyan(self._opcodes, rjust=12, group=True),
            ns_op=colors.cyan(int(self._best * 1e9 // self._opcodes), rjust=8),
            lines=colors.cyan(self._lines, rjust=12, group=True),
        )

    def format_histogram(self, limit: int = 64, lines: int = 2) -> str:
        bars = []
        for chunk in chunks(self.durations, limit):
            bars.append(math.fsum(chunk) / len(chunk))
        return colors.cyan(make_histogram(bars, lines=lines))
