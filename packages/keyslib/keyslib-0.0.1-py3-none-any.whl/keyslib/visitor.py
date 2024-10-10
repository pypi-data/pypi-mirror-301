#!/usr/bin/env python3
from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from keyslib.parser import (
        Primary,
        Keyword,
        Modifier,
        Mask,
        Combo,
        KeySequence,
        Doctag,
        Docstring,
    )


class Visitor(metaclass=ABCMeta):
    """Visitor base class for processing key expressions.

    This can be extended to handle different functionality and output formats for
    key expressions. For example, the Printer class, which formats any key
    expression back into a text sequence.
    """

    @abstractmethod
    def visit_primary(self, expr: Primary) -> str: ...

    @abstractmethod
    def visit_keyword(self, expr: Keyword) -> str: ...

    @abstractmethod
    def visit_modifier(self, expr: Modifier) -> str: ...

    @abstractmethod
    def visit_mask(self, expr: Mask) -> str: ...

    @abstractmethod
    def visit_combo(self, expr: Combo) -> str: ...

    @abstractmethod
    def visit_key_sequence(self, expr: KeySequence) -> str: ...

    @abstractmethod
    def visit_doctag(self, expr: Doctag) -> str: ...

    @abstractmethod
    def visit_docstring(self, expr: Docstring) -> str: ...
