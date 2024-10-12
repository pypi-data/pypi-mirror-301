import ast
from textwrap import dedent
from unittest.mock import ANY

from kotoha.core import ArgumentConcreteTypeHintChecker


class TestArgumentConcreteTypeHintChecker:
    def test_KTH000(self):
        code = dedent(
            """\
        from collections.abc import Iterable

        print("Hello, world!")


        def plus_one_ng(numbers: list[int]) -> list[int]:
            return [n + 1 for n in numbers]


        def plus_one_ok(numbers: Iterable[int]) -> list[int]:
            return [n + 1 for n in numbers]
        """
        )

        checker = ArgumentConcreteTypeHintChecker()
        checker.visit(ast.parse(code))

        assert len(checker.errors) == 1
        assert checker.errors[0] == (6, 16, ANY)
        assert checker.errors[0][2].startswith("KTH000")

    def test_KTH000_none_annotation(self):
        code = dedent(
            """\
        def plus_one_ng(numbers: list[int], dummy) -> list[int]:
            return [n + 1 for n in numbers]
        """
        )

        checker = ArgumentConcreteTypeHintChecker()
        checker.visit(ast.parse(code))

        assert len(checker.errors) == 1

    def test_KTH000_name_object_case(self):
        # Fix `AttributeError: 'Name' object has no attribute 'value'`
        code = dedent(
            """\
        def run(code: str) -> None:
            ...
        """
        )
        checker = ArgumentConcreteTypeHintChecker()
        checker.visit(ast.parse(code))

        assert len(checker.errors) == 0
