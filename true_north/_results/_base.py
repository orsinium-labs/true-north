from __future__ import annotations
import sys
from typing import TextIO
from ._formatters import TICKS


class BaseResult:
    def print(self, stream: TextIO = sys.stdout, indent: int = 4) -> None:
        prefix = ' ' * indent
        for warning in self.format_warnings():
            print(prefix + warning, file=stream)
        print(prefix + self.format_text(), file=stream)
        histogram = self.format_histogram()
        if len(set(histogram) & set(TICKS)) > 1:
            print(prefix + histogram, file=stream)

    def format_text(self) -> str:
        """Represent the result as a human-friendly text.
        """
        raise NotImplementedError

    def format_warnings(self) -> list[str]:
        return []

    def format_histogram(self, limit: int = 64) -> str:
        raise NotImplementedError
