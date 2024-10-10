#!/usr/bin/env python3
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
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


class Printer(Visitor):
    """Key expression printer.

    Given an expression, this will format and return it in string format. This
    format is unique and can be passed back into the expression class to
    re-instantiate it, and is used for the expression's to_str method:

    KeySequence.from_str(KeySequence("(ctrl|alt)c+b #editor Foobar").to_str())
    """

    def to_str(self, expr: Expr) -> str:
        return expr.accept(self)

    def print(self, expr: Expr) -> None:
        print(self.to_str(expr))

    def accept(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_primary(self, expr: Primary) -> str:
        return expr.value

    def visit_keyword(self, expr: Keyword) -> str:
        return f"<{expr.value.name.lower()}>"

    def visit_modifier(self, expr: Modifier) -> str:
        return expr.value.name.lower()

    def visit_mask(self, expr: Mask) -> str:
        modifier = expr.modifier.accept(self)

        if expr.mask:
            mask = expr.mask.accept(self)
            modifier += f"|{mask}"

        return modifier

    def visit_combo(self, expr: Combo) -> str:
        key = expr.key.accept(self)

        if expr.mask:
            mask = expr.mask.accept(self)
            return f"({mask}){key}"
        else:
            return key

    def visit_key_sequence(self, expr: KeySequence) -> str:
        combo = expr.combo.accept(self)

        if expr.key_sequence:
            key_sequence = expr.key_sequence.accept(self)
            combo += f"+{key_sequence}"

        if expr.doctag:
            doctag = expr.doctag.accept(self)
            combo += f" #{doctag}"

        return combo

    def visit_docstring(self, expr: Docstring) -> str:
        return expr.description

    def visit_doctag(self, expr: Doctag) -> str:
        tag = expr.group if expr.group != "default" else ""
        if expr.docstring:
            docstring = expr.docstring.accept(self)
            tag += f" {docstring}"

        return tag
