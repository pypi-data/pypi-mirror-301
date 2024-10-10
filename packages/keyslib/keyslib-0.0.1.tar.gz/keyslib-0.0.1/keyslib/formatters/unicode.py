#!/usr/bin/env python3
from __future__ import annotations

from keyslib.parser import (
    Expr,
    Primary,
    Keyword,
    Modifier,
    Mask,
    Combo,
    KeySequence,
    Doctag,
    Docstring,
)

from keyslib.visitor import Visitor


# NOTE: For JSON encoding, there is a json.encoder.ESCAPE_DCT, which holds all
# the expected escapes (ie (ctrl)b -> 0x02 -> \x02 -> \u0002). If they are escaped
# here, they will just be double escaped.
# https://github.com/python/cpython/blob/3.12/Lib/json/encoder.py#L30
class UnicodeFormatter(Visitor):
    r"""Unicode formatter.

    This will format all key sequences into their unicode equivalents. This includes
    handling for ctrl/alt masks and some keyword handling for keywords which have
    single unicode code point equivalents.
    (ctrl)b+c -> \x02c

    For JSON encoding, there is a json.encoder.ESCAPE_DCT, which holds all
    the expected escapes. If they are escaped here, they will just be double escaped.

    This is relevant when using the unicode formatter in things like VSCode's
    workbench.action.terminal.sendSequence command:

    (ctrl)b+c -> \x02c -> \u0002c (after JSON serialization)

    In this case, the formatter returns \x02b, which is transparently formatted
    to the 4 digit code point representation within the encoder.

    https://github.com/python/cpython/blob/3.12/Lib/json/encoder.py#L30
    """

    def to_str(self, expr: Expr) -> str:
        return expr.accept(self)

    def print(self, expr: Expr) -> None:
        print(self.to_str(expr))

    def accept(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_primary(self, expr: Primary) -> str:
        return ""

    def visit_keyword(self, expr: Keyword) -> str:
        return ""

    def visit_modifier(self, expr: Modifier) -> str:
        return ""

    def visit_mask(self, expr: Mask) -> str:
        return ""

    def visit_combo(self, expr: Combo) -> str:
        code_point = expr.key.unicode()

        if expr.mask:
            code_point = expr.mask.unicode_mask(code_point)

        return chr(code_point)

    def visit_key_sequence(self, expr: KeySequence) -> str:
        combo = expr.combo.accept(self)

        if expr.key_sequence:
            combo += expr.key_sequence.accept(self)

        return combo

    def visit_docstring(self, expr: Docstring) -> str:
        return ""

    def visit_doctag(self, expr: Doctag) -> str:
        return ""


class UnicodeHexFormatter(Visitor):
    """Unicode formatter.

    This will format all key sequences into their unicode hex equivalents. This includes
    handling for ctrl/alt masks and some keyword handling for keywords which have
    single unicode code point equivalents:
    (ctrl)b+c -> 0x02 0x63

    This can be used with the -H flag to tmux send-keys.
    """

    def to_str(self, expr: Expr) -> str:
        return expr.accept(self)

    def print(self, expr: Expr) -> None:
        print(self.to_str(expr))

    def accept(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_primary(self, expr: Primary) -> str:
        return ""

    def visit_keyword(self, expr: Keyword) -> str:
        return ""

    def visit_modifier(self, expr: Modifier) -> str:
        return ""

    def visit_mask(self, expr: Mask) -> str:
        return ""

    def visit_combo(self, expr: Combo) -> str:
        code_point = expr.key.unicode()

        if expr.mask:
            code_point = expr.mask.unicode_mask(code_point)

        return f"{hex(code_point)}"

    def visit_key_sequence(self, expr: KeySequence) -> str:
        combo = expr.combo.accept(self)

        if expr.key_sequence:
            combo += f" {expr.key_sequence.accept(self)}"

        return combo

    def visit_docstring(self, expr: Docstring) -> str:
        return ""

    def visit_doctag(self, expr: Doctag) -> str:
        return ""
