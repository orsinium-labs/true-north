from __future__ import annotations

import inspect
import sys
from functools import cached_property
from pathlib import Path
from typing import Callable, Iterator, TextIO

from ._check import Check, Func
from ._colors import DEFAULT_COLORS, Colors
from ._result import Result


class Group:
    """Collection of benchmarks.

    If `name` is not specified, file name and line number will be used instead.
    """
    _name: str | None
    _checks: list[Check]
    _frame: inspect.Traceback

    def __init__(self, name: str | None = None) -> None:
        self._name = name
        self._checks = []

        frame = inspect.currentframe()
        assert frame is not None
        frame = frame.f_back
        if frame is None:
            raise RuntimeError('cannot find the caller')
        self._frame = inspect.getframeinfo(frame)

    @cached_property
    def name(self) -> str:
        if self._name:
            return self._name
        fname = Path(self._frame.filename).name
        return f'{fname}:{self._frame.lineno}'

    def add(
        self,
        name: str | None = None,
        loops: int | None = None,
        repeats: int = 5,
        min_time: float = .2,
    ) -> Callable[[Func], Check]:
        """Register a new benchmark function in the group.

        The first registered benchmark will be used as the baseline for all others.

        Args:
            name: if not specified, the function name will be used.
            loops: how many times to run the benchmark in each repeat.
                If not specified, will be automatically detected
                to make each repet last at least min_time seconds.
            repeats: how many times repeat the benchmark (all loops).
                The results will show only the best repeat
                to reduce how external factors affect the results.
            min_time: the minimum run time to target if `loops` is not specified.
        """
        def wrapper(func: Func) -> Check:
            check = Check(
                func=func,
                name=name,
                loops=loops,
                repeats=repeats,
                min_time=min_time,
            )
            self._checks.append(check)
            return check

        return wrapper

    def print(
        self,
        stream: TextIO = sys.stdout,
        colors: Colors = DEFAULT_COLORS,
    ) -> None:
        """Run all benchmarks in the group and print their results.
        """
        base_time: float | None = None
        print(colors.blue(self.name), file=stream)
        for check in self._checks:
            print(f'  {colors.magenta(check.name)}', file=stream)
            result = check.run()
            text = result.get_text(colors=colors, base_time=base_time)
            print(text, file=stream)
            if base_time is None:
                base_time = result.best

    def iter(self) -> Iterator[Result]:
        """Iterate over all benchmarks and run them.
        """
        for check in self._checks:
            yield check.run()
