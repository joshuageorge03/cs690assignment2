"""Step 2: split the codebase into chunks, one per function or method.

YOUR CODE. Read HANDOUT.md, Step 2, first.
Check your work with:  pytest tests/test_split.py
"""

from __future__ import annotations

import ast  # noqa: F401  (you will need it)
from pathlib import Path

from askcode import CORPUS_DIR
from askcode.core import Chunk


def split_file(path: Path, root: Path) -> list[Chunk]:
    """Return one Chunk for every function and method in the Python file at `path`.

    Rules. The tests check every one.

    1. Make a chunk for each `def` or `async def` that sits directly in the module,
       and for each `def` or `async def` that sits directly in a class that sits
       directly in the module. Nothing else becomes a chunk: not code outside
       functions, not a class with no methods, not a function nested inside another
       function, not a class nested inside a class, and not a function defined inside
       an `if`, `try`, `for`, `while` or `with` block at module level.
    2. name is the function name, or "ClassName.method_name" for a method.
    3. start_line is the line of the `def`, or the line of the first decorator if the
       function has decorators. end_line is the last line of the function.
       Both count from 1.
    4. text is exactly the source lines start_line to end_line, joined with "\\n".
       Split the file's text on "\\n" (not with str.splitlines) so your line numbers
       agree with the ones ast reports.
    5. file is the path of `path` relative to `root`, written with forward slashes,
       e.g. "sessions.py" or "sub/module.py".
    6. Return the chunks in the order they appear in the file.

    Hint: ast.parse(source) gives you a tree. tree.body lists the top-level
    statements. A function node has .name, .lineno, .end_lineno and .decorator_list,
    and each decorator node has its own .lineno. A class node has .name and .body.
    Read the file with encoding="utf-8".
    """
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    lines = source.split("\n")

    chunks = []

    def add_chunk(node, name):
        start_line = node.lineno

        if node.decorator_list:
            start_line = min(
                decorator.lineno
                for decorator in node.decorator_list
            )

        end_line = node.end_lineno

        text = "\n".join(
            lines[start_line - 1:end_line]
        )

        chunks.append(
            Chunk(
                file=path.relative_to(root).as_posix(),
                name=name,
                start_line=start_line,
                end_line=end_line,
                text=text,
            )
        )

    for node in tree.body:
        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        ):
            add_chunk(node, node.name)

        elif isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(
                    item,
                    (ast.FunctionDef, ast.AsyncFunctionDef),
                ):
                    add_chunk(
                        item,
                        f"{node.name}.{item.name}",
                    )

    return chunks
    

def split_corpus(root: Path = CORPUS_DIR) -> list[Chunk]:
    """Return the chunks of every .py file under `root`, including subfolders.

    Process the files in order of their relative path, written with forward slashes
    and sorted as plain strings. Keep each file's chunks in file order.
    For the requests codebase this returns 230 chunks.
    """
    files = sorted(
        root.rglob("*.py"),
        key=lambda path: path.relative_to(root).as_posix(),
    )
    chunks = []

    for path in files:
        chunks.extend(split_file(path, root))
    return chunks
