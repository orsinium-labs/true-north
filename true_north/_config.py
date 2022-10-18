from __future__ import annotations

import sys
from dataclasses import dataclass, replace
from typing import TextIO


@dataclass(frozen=True)
class Config:
    stream: TextIO = sys.stdout
    opcodes: bool = False
    allocations: bool = False
    histogram_lines: int | None = None

    def evolve(self, **kwargs) -> Config:
        return replace(self, **kwargs)


DEFAULT_CONFIG = Config()
