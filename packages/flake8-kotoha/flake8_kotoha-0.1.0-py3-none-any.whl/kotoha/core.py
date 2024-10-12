import ast

KTH101 = (
    "KTH101 "
    "Type hint with abstract type `collections.abc.Iterable` or "
    "`collections.abc.Sequence`, "
    "instead of concrete type `list`"
)
KTH102 = (
    "KTH102 "
    "Type hint with abstract type `collections.abc.Iterable` or "
    "`collections.abc.Sequence`, "
    "instead of concrete type `tuple`"
)
KTH103 = (
    "KTH103 "
    "Type hint with abstract type `collections.abc.Iterable`"
    "instead of concrete type `set`"
)
KTH104 = (
    "KTH104 "
    "Type hint with abstract type `collections.abc.Iterable`"
    "instead of concrete type `dict`"
)

LineNumber = int
ColumnOffset = int
ErrorMessage = str


class ArgumentConcreteTypeHintChecker(ast.NodeVisitor):
    _concrete_type_hint_error_codes: dict[str, ErrorMessage] = {
        "list": KTH101,
        "tuple": KTH102,
        "set": KTH103,
        "dict": KTH104,
    }

    def __init__(self) -> None:
        self.errors: list[tuple[LineNumber, ColumnOffset, ErrorMessage]] = []

    def visit_arg(self, node: ast.arg) -> None:
        if node.annotation is not None:
            annotation: ast.expr = node.annotation
            if (
                hasattr(annotation, "value")
                and annotation.value.id in self._concrete_type_hint_error_codes
            ):
                self.errors.append(
                    (
                        node.lineno,
                        node.col_offset,
                        self._concrete_type_hint_error_codes[
                            annotation.value.id
                        ],
                    )
                )
        self.generic_visit(node)


def run(code: str) -> None:
    tree = ast.parse(code)
    ArgumentConcreteTypeHintChecker().visit(tree)
