from __future__ import annotations

import sys
from typing import TextIO

from ._formatters import TICKS


class BaseResult:
    __slots__ = ()

    def print(
        self,
        stream: TextIO = sys.stdout,
        indent: int = 4,
        histogram_lines: int | None = None,
    ) -> None:
        prefix = ' ' * indent
        for warning in self.format_warnings():
            print(prefix + warning, file=stream)
        print(prefix + self.format_text(), file=stream)
        if histogram_lines is not None:
            hist = self.format_histogram(lines=histogram_lines)
            if len(set(hist) & set(TICKS)) > 1:
                print(prefix + hist, file=stream)

    def format_text(self) -> str:
        """Represent the result as a human-friendly text.
        """
        raise NotImplementedError

    def format_warnings(self) -> list[str]:
        return []

    def format_histogram(self, limit: int = 64, lines: int = 2) -> str:
        raise NotImplementedError
