from __future__ import annotations
from dataclasses import dataclass
import sys
from typing import TextIO

from ._colors import Colors, DEFAULT_COLORS
from ._result import Result


@dataclass(frozen=True)
class Results:
    name: str
    results: list[Result]

    def print(
        self,
        stream: TextIO = sys.stdout,
        colors: Colors = DEFAULT_COLORS,
    ) -> None:
        """Print all results.
        """
        base_time: float | None = None
        print(colors.blue(self.name), file=stream)
        for result in self.results:
            print(f'  {colors.magenta(result.name)}', file=stream)
            text = result.get_text(colors=colors, base_time=base_time)
            print(text, file=stream)
            if base_time is None:
                base_time = result.best
