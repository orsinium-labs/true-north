from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Any


RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
END = '\033[0m'


@dataclass(frozen=True)
class Colors:
    disabled: bool = bool(os.environ.get('NO_COLOR'))

    def green(self, text: Any) -> str:
        if self.disabled:
            return str(text)
        return f'{GREEN}{text}{END}'

    def yellow(self, text: Any) -> str:
        if self.disabled:
            return str(text)
        return f'{YELLOW}{text}{END}'

    def red(self, text: Any) -> str:
        if self.disabled:
            return str(text)
        return f'{RED}{text}{END}'

    def blue(self, text: Any) -> str:
        if self.disabled:
            return str(text)
        return f'{BLUE}{text}{END}'

    def magenta(self, text: Any) -> str:
        if self.disabled:
            return str(text)
        return f'{MAGENTA}{text}{END}'

    def cyan(self, text: Any) -> str:
        if self.disabled:
            return str(text)
        return f'{CYAN}{text}{END}'


DEFAULT_COLORS = Colors()
