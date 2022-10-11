

from __future__ import annotations

from dataclasses import dataclass

from .._colors import DEFAULT_COLORS, Colors


@dataclass
class OpcodesResult:
    opcodes: int
    lines: int
    best: float

    def format(self, colors: Colors = DEFAULT_COLORS) -> str:
        """Generate a human-friendly representation of opcodes.
        """
        opcodes = colors.cyan(self.opcodes, rjust=12, group=True)
        ns_op = colors.cyan(int(self.best * 1e9 // self.opcodes), rjust=8)
        lines = colors.cyan(self.lines, rjust=12, group=True)
        return f'    {opcodes} ops {ns_op} ns/op {lines} lines'
