from __future__ import annotations

import inspect
import os
from time import perf_counter
from typing import Callable

from ._check import Check, Func
from ._colors import colors
from ._config import DEFAULT_CONFIG, Config
from ._loopers import Timer


class Group:
    """Collection of benchmarks.

    If `name` is not specified, file name and line number will be used instead.
    """
    __slots__ = ('name', '_checks')
    name: str
    _checks: list[Check]

    def __init__(self, name: str | None = None) -> None:
        self._checks = []

        if name is None:
            frame = inspect.currentframe()
            assert frame is not None
            frame = frame.f_back
            if frame is None:
                name = '???'
            else:
                file_name = os.path.basename(frame.f_code.co_filename)
                name = f'{file_name}:{frame.f_lineno}'
        self.name = name

    def add(
        self,
        func: Func | None = None,
        *,
        name: str | None = None,
        loops: int | None = None,
        repeats: int = 5,
        min_time: float = .2,
        timer: Timer = perf_counter,
    ) -> Callable[[Func], Check]:
        """Register a new benchmark function in the group.

        The first registered benchmark will be used as the baseline for all others.

        Args:
            name: if not specified, the function name will be used.
            loops: how many times to run the benchmark in each repeat.
                If not specified, will be automatically detected
                to make each repeat last at least min_time seconds.
            repeats: how many times repeat the benchmark (all loops).
                The results will show only the best repeat
                to reduce how external factors affect the results.
            min_time: the minimum run time to target if `loops` is not specified.
            timer: function used to get the current time.

        """
        def wrapper(func: Func) -> Check:
            check = Check(
                func=func,
                name=name or func.__name__,
                loops=loops,
                repeats=repeats,
                min_time=min_time,
                timer=timer,
            )
            self._checks.append(check)
            return check

        if func is not None:
            # IDK how to make a proper `@overload` signature
            # without duplicating all arguments.
            # Just look at how signature for `open` is declared.
            return wrapper(func)  # type: ignore[return-value]
        return wrapper

    def print(self, config: Config = DEFAULT_CONFIG) -> None:
        """Run all benchmarks in the group and print their results.

        Args:
            stream: the stream where to write all output.
                Default is stdout.
            opcodes: count opcodes. Slow but reproducible.
            allocations: track memory allocations. Slow but interesting.
        """
        base_time: float | None = None
        print(colors.blue(self.name), file=config.stream)
        for check in self._checks:
            result = check.print(config=config, base_time=base_time)
            if base_time is None:
                base_time = result.best
