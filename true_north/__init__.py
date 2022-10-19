"""Beautiful and pythonic benchmarks engine.

Links:
    https://github.com/orsinium-labs/true-north
    https://true-north.orsinium.dev/
"""
from . import types
from ._colors import disable_colors, enable_colors, reset_colors
from ._config import Config
from ._group import Group


__version__ = '0.3.0'
__all__ = [
    'disable_colors',
    'enable_colors',
    'Config',
    'Group',
    'reset_colors',
    'types',
]
