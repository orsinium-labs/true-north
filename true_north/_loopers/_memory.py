from __future__ import annotations

import tracemalloc
from collections import Counter
from dataclasses import dataclass, field
from typing import Iterator

from ._common import tracer_context


@dataclass
class MemoryLooper:
    period: int
    loops: int = 1
    lines: int = 0
    totals: list[int] = field(default_factory=list)
    allocs: list[Counter[str]] = field(default_factory=list)
    _prev_allocs: Counter[str] = field(default_factory=Counter)

    def ltracer(self, frame, event: str, arg):
        """Local tracer attached to each function.
        """
        if event == 'line' and frame.f_code.co_filename != __file__:
            self.lines += 1
            if self.lines % self.period == 0:
                # gc.collect()
                snapshot = tracemalloc.take_snapshot()
                total = 0
                allocs: Counter[str] = Counter()
                for trace in snapshot.traces:
                    total += trace.size
                    file_name = trace.traceback[-1].filename
                    allocs[file_name] += 1
                self.totals.append(total)
                diff = allocs - self._prev_allocs
                self.allocs.append(diff)
                self._prev_allocs = allocs

    def gtracer(self, frame, event: str, arg):
        """Global tracer executed for all functions.
        """
        if event == 'call':
            return self.ltracer

    def __iter__(self) -> Iterator[int]:
        tracemalloc.start()
        self.totals = []
        with tracer_context(self.gtracer):
            for i in range(self.loops):
                yield i
        tracemalloc.stop()
