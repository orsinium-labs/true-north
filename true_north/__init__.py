"""Beautiful and pythonic benchmarks engine.
"""
from . import types
from ._colors import disable_colors, enable_colors, reset_colors
from ._group import Group


__version__ = '0.2.0'
__all__ = [
    'disable_colors',
    'enable_colors',
    'Group',
    'reset_colors',
    'types',
]
