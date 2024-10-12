import ast
from textwrap import dedent
from unittest.mock import ANY

from kotoha.core import ArgumentConcreteTypeHintChecker


class TestArgumentConcreteTypeHintChecker:
    def test_KTH101(self) -> None:
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
        assert checker.errors[0][2].startswith("KTH101")

    def test_KTH102(self) -> None:
        code = dedent(
            """\
        def plus_one(numbers: tuple[int]) -> list[int]:
            return [n + 1 for n in numbers]
        """
        )

        checker = ArgumentConcreteTypeHintChecker()
        checker.visit(ast.parse(code))

        assert len(checker.errors) == 1
        assert checker.errors[0] == (1, 13, ANY)
        assert checker.errors[0][2].startswith("KTH102")

    def test_KTH103(self) -> None:
        code = dedent(
            """\
        def plus_one(numbers: set[int]) -> list[int]:
            return [n + 1 for n in numbers]
        """
        )

        checker = ArgumentConcreteTypeHintChecker()
        checker.visit(ast.parse(code))

        assert len(checker.errors) == 1
        assert checker.errors[0] == (1, 13, ANY)
        assert checker.errors[0][2].startswith("KTH103")

    def test_KTH104(self) -> None:
        code = dedent(
            """\
        def plus_one(numbers: dict[int, str]) -> list[int]:
            return [n + 1 for n in numbers]
        """
        )

        checker = ArgumentConcreteTypeHintChecker()
        checker.visit(ast.parse(code))

        assert len(checker.errors) == 1
        assert checker.errors[0] == (1, 13, ANY)
        assert checker.errors[0][2].startswith("KTH104")

    def test_not_raise_error_to_none(self) -> None:
        code = dedent(
            """\
        def func_parameter_type_hint_is_none(numbers) -> list[int]:
            return [n + 1 for n in numbers]
        """
        )

        checker = ArgumentConcreteTypeHintChecker()
        checker.visit(ast.parse(code))

        assert len(checker.errors) == 0

    def test_not_raise_error_to_name_object(self) -> None:
        # Fix `AttributeError: 'Name' object has no attribute 'value'`
        code = dedent(
            """\
        def func_parameter_type_hint_name_case(code: str) -> None:
            ...
        """
        )
        checker = ArgumentConcreteTypeHintChecker()
        checker.visit(ast.parse(code))

        assert len(checker.errors) == 0
