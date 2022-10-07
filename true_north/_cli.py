from __future__ import annotations

import argparse
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Iterator, NoReturn, TextIO

from ._colors import DEFAULT_COLORS, Colors
from ._group import Group


try:
    import ipdb as pdb
except ImportError:
    import pdb  # type: ignore


def get_paths(path: Path) -> Iterator[Path]:
    """Recursively yields python files.
    """
    if not path.exists():
        raise FileNotFoundError(str(path))
    if path.is_file():
        if path.suffix == '.py':
            yield path
        return
    for subpath in path.iterdir():
        if subpath.name[0] == '.':
            continue
        if subpath.name == '__pycache__':
            continue
        yield from get_paths(subpath)


def run_all_groups(path: Path, args: argparse.Namespace, stdout: TextIO) -> None:
    content = path.read_text()
    globals: dict[str, object] = {}
    code = compile(content, filename=str(path), mode='exec')
    exec(code, globals)
    if args.no_color:
        colors = Colors(disabled=True)
    else:
        colors = DEFAULT_COLORS
    for group in globals.values():
        if not isinstance(group, Group):
            continue
        if args.groups and group.name not in args.groups:
            continue
        group.print(
            stream=stdout,
            opcodes=args.opcodes,
            colors=colors,
        )


def main(argv: list[str], stdout: TextIO) -> int:
    parser = ArgumentParser()
    parser.add_argument('paths', nargs='+')
    parser.add_argument(
        '--opcodes', action='store_true',
        help='Count opcodes. Slow but reproducible.'
    )
    parser.add_argument(
        '--no-color', action='store_true',
        help='Write a boring one-color output.'
    )
    parser.add_argument(
        '--pdb', action='store_true',
        help='Run PDB on failure.'
    )
    parser.add_argument(
        '--group', dest='groups', nargs='*',
        help='The group name to run. Can specify multiple values.'
    )
    args = parser.parse_args(argv)
    try:
        for root in args.paths:
            for path in get_paths(Path(root)):
                run_all_groups(path, args=args, stdout=stdout)
    except KeyboardInterrupt:
        print('Interrupted')
        return 1
    except Exception:
        if args.pdb:
            pdb.post_mortem()
        raise
    return 0


def entrypoint() -> NoReturn:
    sys.exit(main(argv=sys.argv[1:], stdout=sys.stdout))
