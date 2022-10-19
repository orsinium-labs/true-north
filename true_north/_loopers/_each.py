from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from ._common import Timer


@dataclass
class EachLooper:
    """Iterator that tracks the execution time of each iteration.
    """
    loops: int
    timer: Timer
    timings: list[float]

    def __iter__(self) -> Iterator[int]:
        self.timings = []
        for i in range(self.loops):
            start = self.timer()
            yield i
            stop = self.timer()
            self.timings.append(stop - start)
