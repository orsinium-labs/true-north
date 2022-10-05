from __future__ import annotations
import inspect
from dataclasses import dataclass
import sys
from types import FrameType
from typing import Callable, Iterator


Timer = Callable[[], float]


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
    count: int = 0
    active: bool = False

    def callback(self, frame: FrameType, event: str, arg):
        frame.f_trace_opcodes = True
        if event == 'opcode' and frame.f_code.co_filename != __file__:
            self.count += 1
        elif event == 'return':
            frame.f_trace_opcodes = True
            frame.f_trace = None

    def noop(self, frame, event: str, arg):
        if self.active and event == 'call':
            return self.callback

    def __iter__(self) -> Iterator[int]:
        frame = inspect.currentframe()
        assert frame
        frame = frame.f_back
        assert frame

        sys.settrace(self.noop)         # enable tracing globally
        frame.f_trace = self.callback   # trace the benchmarking function
        frame.f_trace_opcodes = True    # enable opcode tracing
        self.active = True

        self.count = 0
        for i in range(self.loops):
            yield i

        frame.f_trace = None
        frame.f_trace_opcodes = False
        self.active = False
