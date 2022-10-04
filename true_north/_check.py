from __future__ import annotations
import ast

from dataclasses import dataclass
from functools import cached_property
import inspect
from pathlib import Path
from timeit import Timer
from typing import Callable
from ._result import Result


class setup:
    """Context manager to mark preparation work that must be excluded from benchmark.

    Everything inside the context won't be measured.
    Must be called first in the test function.
    """

    def __enter__(self) -> None:
        raise RuntimeError('setup was not statically detected')

    def __exit__(self, *_) -> None:
        pass


@dataclass
class Check:
    name: str | None
    func: Callable[..., None]
    frame: inspect.Traceback
    loops: int | None
    repeats: int
    globals: dict

    @cached_property
    def node(self) -> ast.FunctionDef:
        tree = ast.parse(
            source=Path(self.frame.filename).read_text(),
            filename=self.frame.filename,
        )
        lines = {self.frame.lineno, self.frame.lineno + 1}
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue
            if node.lineno not in lines:
                continue
            return node
        raise LookupError('cannot find AST node for function definition')

    @cached_property
    def timer(self) -> Timer:
        bench_body = self.node.body
        setup_body = self._get_setup(bench_body[0])
        if setup_body:
            bench_body = bench_body[1:]
        return Timer(
            setup=self._ast_to_func(setup_body),
            stmt=self._ast_to_func(bench_body),
        )

    def _get_setup(self, stmt: ast.stmt) -> list[ast.stmt]:
        # must by a `with` statement with one item
        if not isinstance(stmt, ast.With):
            return []
        if len(stmt.items) != 1:
            return []

        # # must have name `setup`
        expr = stmt.items[0].context_expr
        if not isinstance(expr, ast.Call):
            return []
        expr = expr.func
        name = ''
        if isinstance(expr, ast.Name):
            name = expr.id
        if isinstance(expr, ast.Attribute):
            name = expr.attr
        if name != 'setup':
            return []

        return stmt.body

    def _ast_to_func(self, nodes: list[ast.stmt]) -> Callable[[], None]:
        module = ast.Module(body=nodes, type_ignores=[])
        bytecode = compile(module, filename='<ast>', mode='exec')

        def executor() -> None:
            exec(bytecode, self.globals)

        return executor

    def run(self) -> Result:
        loops = self.loops
        if loops is None:
            loops, _ = self.timer.autorange(None)
        raw_timings = self.timer.repeat(repeat=self.repeats, number=loops)
        assert len(raw_timings) == self.repeats
        return Result(
            name=self.name or self.func.__name__,
            timings=[dt / loops for dt in raw_timings],
            loops=loops,
        )
