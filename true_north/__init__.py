"""Beautiful and pythonic benchmarks engine.

Links:
    https://github.com/orsinium-labs/true-north
    https://true-north.orsinium.dev/
"""
from . import types
from ._cli import entrypoint, main
from ._colors import disable_colors, enable_colors, reset_colors
from ._config import Config
from ._group import Group


__version__ = '0.3.0'
__all__ = [
    'Config',
    'disable_colors',
    'enable_colors',
    'entrypoint',
    'Group',
    'main',
    'reset_colors',
    'types',
]
