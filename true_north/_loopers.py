from __future__ import annotations
from contextlib import contextmanager

import inspect
import sys
from dataclasses import dataclass
import tracemalloc
from types import FrameType
from typing import Callable, Iterator


Timer = Callable[[], float]


@contextmanager
def tracer_context(tracer: Callable) -> Iterator:
    old_tracer = sys.gettrace()
    sys.settrace(tracer)
    try:
        yield
    finally:
        sys.settrace(old_tracer)


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


@dataclass
class OpcodeLooper:
    loops: int
    opcodes: int = 0
    lines: int = 0

    def ltracer(self, frame: FrameType, event: str, arg):
        if event == 'return':
            frame.f_trace_opcodes = False
            frame.f_trace = None
        elif frame.f_code.co_filename != __file__:
            frame.f_trace_opcodes = True
            if event == 'opcode':
                self.opcodes += 1
            elif event == 'line':
                self.lines += 1

    def gtracer(self, frame, event: str, arg):
        if event == 'call':
            return self.ltracer

    def __iter__(self) -> Iterator[int]:
        frame = inspect.currentframe()
        assert frame
        frame = frame.f_back
        assert frame

        frame.f_trace = self.ltracer    # trace the benchmarking function
        frame.f_trace_opcodes = True    # enable opcode tracing
        self.active = True

        with tracer_context(self.gtracer):
            for i in range(self.loops):
                yield i

        frame.f_trace = None
        frame.f_trace_opcodes = False


@dataclass
class MemoryLooper:
    loops: int
    snapshots: list[int]
    period: int
    lines: int = 0

    def ltracer(self, frame, event: str, arg):
        """Local tracer attached to each function.
        """
        if event == 'line' and frame.f_code.co_filename != __file__:
            self.lines += 1
            if self.lines % self.period == 0:
                snapshot = tracemalloc.take_snapshot()
                total = 0
                for trace in snapshot.traces:
                    total += trace.size
                self.snapshots.append(total)

    def gtracer(self, frame, event: str, arg):
        """Global tracer executed for all functions.
        """
        if event == 'call':
            return self.ltracer

    def __iter__(self) -> Iterator[int]:
        frame = inspect.currentframe()
        assert frame
        frame = frame.f_back
        assert frame

        tracemalloc.start()
        self.snapshots = []
        with tracer_context(self.gtracer):
            for i in range(self.loops):
                yield i
        tracemalloc.stop()
