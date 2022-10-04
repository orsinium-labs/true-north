from __future__ import annotations
from dataclasses import dataclass, field
import inspect
from typing import Callable
from ._check import Check
from ._results import Results

Func = Callable[[], None]


@dataclass
class Group:
    name: str | None = None

    _checks: list[Check] = field(default_factory=list)

    def add(
        self,
        name: str | None = None,
        loops: int | None = None,
        repeats: int = 5,
    ) -> Callable[[Func], Check]:
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
        name = self.name or '?'
        results = []
        for check in self._checks:
            result = check.run()
            results.append(result)
        return Results(
            name=name,
            results=results,
        )
