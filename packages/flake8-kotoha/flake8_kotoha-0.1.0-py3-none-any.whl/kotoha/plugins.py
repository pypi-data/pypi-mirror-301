import ast
from collections.abc import Generator
from typing import Any, Type

import kotoha
from kotoha.core import ArgumentConcreteTypeHintChecker


class Flake8KotohaPlugin:
    name = "flake8-kotoha"
    version = kotoha.__version__

    def __init__(self, tree: ast.AST) -> None:
        self._tree = tree

    def run(self) -> Generator[tuple[int, int, str, Type[Any]], None, None]:
        checker = ArgumentConcreteTypeHintChecker()
        checker.visit(self._tree)

        for lineno, col_offset, message in checker.errors:
            yield (lineno, col_offset, message, type(self))
