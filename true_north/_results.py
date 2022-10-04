from __future__ import annotations
from dataclasses import dataclass
import sys
from typing import TextIO

from ._result import Result


@dataclass(frozen=True)
class Results:
    name: str
    results: list[Result]

    def print(self, stream: TextIO = sys.stdout) -> None:
        """Print all results.
        """
        print(self.name, file=stream)
        for result in self.results:
            print(f'  {result.name}', file=stream)
            print(result.text, file=stream)
