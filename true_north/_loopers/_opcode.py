from __future__ import annotations

import inspect
import time
from dataclasses import dataclass, field
from types import FrameType
from typing import Iterator

from ._common import tracer_context


@dataclass
class OpcodeLooper:
    loops: int
    opcodes: int = 0
    lines: int = 0
    timings: list[float] = field(default_factory=list)

    def ltracer(self, frame: FrameType, event: str, arg):
        if event == 'return':
            frame.f_trace_opcodes = False
            frame.f_trace = None
        elif frame.f_code.co_filename != __file__:
            frame.f_trace_opcodes = True
            if event == 'opcode':
                self.opcodes += 1
                self.timings.append(time.perf_counter())
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
