import ast

KTH000 = (
    "KTH000 "
    "concrete type (`list`, `dict`, `set`, `tuple`) in function parameters, "
    "use abstract type (`Iterable`, `Sequence` or `Mapping` "
    "from `collections.abc`)"
)


class ArgumentConcreteTypeHintChecker(ast.NodeVisitor):
    def __init__(self) -> None:
        self.errors: list[tuple[int, int, str]] = []

    def visit_arg(self, node: ast.arg) -> None:
        if node.annotation is not None:
            annotation: ast.expr = node.annotation
            if hasattr(annotation, "value") and annotation.value.id in {
                "list",
                "dict",
                "set",
                "tuple",
            }:
                self.errors.append((node.lineno, node.col_offset, KTH000))
        self.generic_visit(node)


def run(code: str) -> None:
    tree = ast.parse(code)
    ArgumentConcreteTypeHintChecker().visit(tree)
