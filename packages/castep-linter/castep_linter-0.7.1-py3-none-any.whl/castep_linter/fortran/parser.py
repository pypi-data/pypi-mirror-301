"""Tests for Fortran code in CASTEP"""

import pathlib
from typing import Callable, Generator, Optional

import tree_sitter_fortran
from tree_sitter import Language, Parser

from castep_linter.fortran import node_factory
from castep_linter.fortran.fortran_nodes import FortranNode


def get_fortran_parser() -> Parser:
    """Get a tree-sitter-fortran parser from fortran_language_pack"""
    return Parser(Language(tree_sitter_fortran.language()))


class FortranTree:
    """Parsed fortran source code tree"""

    def __init__(self, raw_text: bytes, parser: Optional[Parser] = None):
        if parser is None:
            parser = get_fortran_parser()

        self.raw_text = raw_text
        self.tree = parser.parse(self.raw_text)

    @staticmethod
    def from_file(file: pathlib.Path):
        """Read from a file and return a AST"""
        with file.open("rb") as fd:
            raw_text = fd.read()
        return FortranTree(raw_text)

    def walk(self) -> Generator[FortranNode, None, None]:
        """Traverse a tree-sitter tree in a depth first search"""
        cursor = self.tree.walk()

        reached_root = False
        while not reached_root:
            if cursor.node is None:
                err = "Reached end of tree unexpectedly"
                raise EOFError(err)

            yield node_factory.wrap_node(cursor.node)

            if cursor.goto_first_child():
                continue

            if cursor.goto_next_sibling():
                continue

            retracing = True
            while retracing:
                if not cursor.goto_parent():
                    retracing = False
                    reached_root = True

                if cursor.goto_next_sibling():
                    retracing = False

    def display(self, printfn: Callable):
        """Print the tree for the source file"""
        node_factory.wrap_node(self.tree.root_node).print_tree(printfn)
