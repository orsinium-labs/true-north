

from __future__ import annotations

from dataclasses import dataclass

from .._colors import DEFAULT_COLORS, Colors


@dataclass(frozen=True)
class OpcodesResult:
    """The result of benchmarking opcodes executed by a code.
    """
    opcodes: int    # number of opcodes executed
    lines: int      # number of lines executed (see lnotab_notes.txt in CPython)
    best: float     # the best execution time, used to calculate ns/op.

    def format(self, colors: Colors = DEFAULT_COLORS) -> str:
        """Generate a human-friendly representation of opcodes.
        """
        return '    {opcodes} ops {ns_op} ns/op {lines} lines'.format(
            opcodes=colors.cyan(self.opcodes, rjust=12, group=True),
            ns_op=colors.cyan(int(self.best * 1e9 // self.opcodes), rjust=8),
            lines=colors.cyan(self.lines, rjust=12, group=True),
        )
