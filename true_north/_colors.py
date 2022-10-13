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

    'B  ': CYAN,
    'KiB': GREEN,
    'MiB': YELLOW,
    'GiB': RED,
    'TiB': RED,
}


def _color(color: str) -> Callable[..., str]:
    def colorer(
        self: Colors,
        text: str | float,
        *,
        rjust: int | None = None,
        group: bool = False,
        precision: int | None = None
    ) -> str:
        if precision:
            text = f'{text:.{precision}f}'
        if group and len(str(text)) > 4:
            text = f'{text:,}'.replace(',', '_')
        if rjust:
            text = f'{text:>{rjust}}'
        if self._disabled:
            return str(text)
        return f'{color}{text}{END}'

    return colorer


@dataclass
class Colors:
    """An internal class responsible for coloring console output.
    """
    _disabled: bool = False

    def disable(self) -> None:
        """Print all output in boring white letters.
        """
        self._disabled = True

    def enable(self) -> None:
        """Make all output chad and colorful.
        """
        self._disabled = False

    def reset(self) -> None:
        """Restore the coloring state to the default (NO_COLOR env var).
        """
        self._disabled = bool(os.environ.get('NO_COLOR'))

    def color_unit(self, unit: str) -> str:
        """Color a unit of time (ns) of size (MiB).
        """
        if self._disabled:
            return unit
        return f'{UNITS[unit]}{unit}{END}'

    green = _color(GREEN)
    yellow = _color(YELLOW)
    red = _color(RED)
    blue = _color(BLUE)
    magenta = _color(MAGENTA)
    cyan = _color(CYAN)


# The global singleton instance used by all code.
colors = Colors()
colors.reset()

# public API
disable_colors = colors.disable
enable_colors = colors.enable
reset_colors = colors.reset
