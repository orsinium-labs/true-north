from __future__ import annotations

import sys
from contextlib import contextmanager
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
