from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from ._common import Timer


@dataclass
class TotalLooper:
    """Iterator that tracks the total execution time.
    """
    loops: int
    timer: Timer
    start: float = 0
    stop: float = 0

    def __iter__(self) -> Iterator[int]:
        self.start = self.timer()
        for i in range(self.loops):
            yield i
        self.stop = self.timer()
