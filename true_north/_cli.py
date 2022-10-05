from __future__ import annotations
import argparse

import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Iterator, NoReturn, TextIO

from ._group import Group


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
    for obj in globals.values():
        if isinstance(obj, Group):
            obj.print(stream=stdout, opcodes=args.opcodes)


def main(argv: list[str], stdout: TextIO) -> int:
    parser = ArgumentParser()
    parser.add_argument('paths', nargs='+')
    parser.add_argument(
        '--opcodes', action='store_true',
        help='Count opcodes. Slow but reproducible.'
    )
    args = parser.parse_args(argv)
    for root in args.paths:
        for path in get_paths(Path(root)):
            run_all_groups(path, args=args, stdout=stdout)
    return 0


def entrypoint() -> NoReturn:
    sys.exit(main(argv=sys.argv[1:], stdout=sys.stdout))
