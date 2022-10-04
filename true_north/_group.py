from __future__ import annotations
import inspect
from pathlib import Path
from typing import Callable

from functools import cached_property
from ._check import Check
from ._results import Results

Func = Callable[[], None]


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
    ) -> Callable[[Func], Check]:
        """Register a new benchmark function in the group.

        Args:
            name: if not specified, the function name will be used.
            loops: how many times to run the benchmark in each repeat.
                If not specified, will be automatically detected
                to make each repet last at least 0.2 seconds.
            repeats: how many times repeat the benchmark (all loops).
                The results will show only the best repeat
                to reduce how external factors affect the results.
        """
        frame = inspect.currentframe()
        assert frame is not None
        frame = frame.f_back
        if frame is None:
            raise RuntimeError('cannot find the caller')
        frame_info = inspect.getframeinfo(frame)
        globals = frame.f_globals

        def wrapper(func: Func) -> Check:
            check = Check(
                func=func,
                name=name,
                loops=loops,
                repeats=repeats,
                frame=frame_info,
                globals=globals,
            )
            self._checks.append(check)
            return check

        return wrapper

    def run(self) -> Results:
        """Run all benchmarks in the group.
        """
        results = []
        for check in self._checks:
            result = check.run()
            results.append(result)
        return Results(
            name=self.name,
            results=results,
        )
