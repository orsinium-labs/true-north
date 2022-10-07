from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable


RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
END = '\033[0m'

UNITS = {
    's ': RED,
    'ms': YELLOW,
    'us': GREEN,
    'ns': CYAN,
}


def _color(color: str) -> Callable[..., str]:
    def colorer(
        self: Colors,
        text: str | float,
        *,
        rjust: int | None = None,
        group: bool = False,
    ) -> str:
        if group and len(str(text)) > 4:
            text = f'{text:,}'.replace(',', '_')
        if rjust:
            text = f'{text:>{rjust}}'
        if self.disabled:
            return str(text)
        return f'{color}{text}{END}'

    return colorer


@dataclass(frozen=True)
class Colors:
    disabled: bool = bool(os.environ.get('NO_COLOR'))

    def color_unit(self, unit: str) -> str:
        if self.disabled:
            return unit
        return f'{UNITS[unit]}{unit}{END}'

    green = _color(GREEN)
    yellow = _color(YELLOW)
    red = _color(RED)
    blue = _color(BLUE)
    magenta = _color(MAGENTA)
    cyan = _color(CYAN)


DEFAULT_COLORS = Colors()
