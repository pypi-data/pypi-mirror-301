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

from keyslib.types import ModifierType
from keyslib.visitor import Visitor


class HammerspoonFormatter(Visitor):
    """hammerspoon formatter for key sequences.

    This will format a KeySequence as a call to hs.eventtap.keyStroke, for use
    via the hammerspoon CLI (hs):

    (cmd|shift)p -> hs.eventtap.keyStroke({"cmd", "shift"}, "p");
    (ctrl)b+c -> hs.eventtap.keyStroke({"cmd", "shift"}, "b"); hs.eventtap.keyStroke({}, "c");

    Reference: https://www.hammerspoon.org/docs/hs.eventtap.html#keyStroke
    """

    def to_str(self, expr: Expr) -> str:
        return expr.accept(self)

    def print(self, expr: Expr) -> None:
        print(self.to_str(expr))

    def accept(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_primary(self, expr: Primary) -> str:
        """Format a Primary for a hammerspoon eventtap call.

        Primaries in HS are just quoted unicode chars:
        p -> "p"

        Args:
            expr: Primary. Primary for a Key to be formatted.

        Returns:
            formatted_primary: Primary char formatted for use in a hammerspoon
                eventtap call.
        """

        return f'"{expr.value}"'

    def visit_keyword(self, expr: Keyword) -> str:
        r"""Format a Keyword for a hammerspoon eventtap call.

        Keywords in HS are quoted and must have unicode char equivalents:
        <enter> -> \n

        Args:
            expr: Keyword. Keyword for a Key to be formatted.

        Returns:
            formatted_keyword: Keyword formatted for use in a hammerspoon eventtap
                call.
        """

        char = chr(expr.unicode())

        return f'"{char}"'

    def visit_modifier(self, expr: Modifier) -> str:
        """Format a Modifier for a hammerspoon eventtap call.

        Modifiers are represented by their lowercase names and collected in a
        mask table:
        (ctrl) -> "ctrl"

        Args:
            expr: Modifier. Modifier for a Mask to be formatted.

        Returns:
            formatted_modifier: Modifier formatted for use in a hammerspoon eventtap
                call.
        """

        # hs modifier translation
        # https://www.hammerspoon.org/docs/hs.eventtap.html#keyStroke
        match expr.value:
            case ModifierType.FN:
                mod = "fn"
            case ModifierType.CTRL:
                mod = "ctrl"
            case ModifierType.ALT:
                mod = "alt"
            case ModifierType.CMD:
                mod = "cmd"
            case ModifierType.SHIFT:
                mod = "shift"
            case _:
                raise ValueError(f"Unsupported hammerspoon modifier: {expr}")

        return f'"{mod}"'

    def visit_mask(self, expr: Mask) -> str:
        """Format a Mask for a hammerspoon eventtap call.

        Masks are represented as a table of modifier strings as the first argument
        to a keyStroke call:
        (ctrl|shift) -> "ctrl", "shift"

        Args:
            expr: Mask from a Combo to be formatted.

        Returns:
            formatted_mask: str. Mask formatted for use in a hammerspoon eventtap
                call.
        """

        modifiers = expr.modifier.accept(self)

        if expr.mask:
            modifiers += f", {expr.mask.accept(self)}"

        return modifiers

    def visit_combo(self, expr: Combo) -> str:
        r"""Format a Combo for use in a hammerspoon eventtap call.

        Combos are represented as a call to hs.eventtap.keyStroke, with a table
        of modifiers and a single char representing a primary or keyword as
        the arguments:
        (ctrl|shift)b -> hs.eventtap.keyStroke({"ctrl", "shift"}, "b")
        <enter> -> hs.eventtap.keyStroke({}, "\n")

        Args:
            expr: Combo to be formatted.

        Returns:
            formatted_mask: str. Combo formatted for use in a hammerspoon eventtap
                call.
        """

        if expr.mask:
            mask = expr.mask.accept(self)

            mask = f"{{{mask}}}"
        else:
            # Use empty table for no mask, per HS docs:
            # Note that invoking this function with a table (empty or otherwise)
            # for the modifiers argument will force the release of any modifier
            # keys which have been explicitly created by hs.eventtap.event.newKeyEvent
            # and posted that are still in the "down" state. An explicit nil for
            # this argument will not (i.e. the keystroke will inherit any currently
            # "down" modifiers)
            mask = "{}"

        key = expr.key.accept(self)

        return f"hs.eventtap.keyStroke({mask}, {key})"

    def visit_key_sequence(self, expr: KeySequence) -> str:
        """Format a KeySequence as a hammerspoon eventtap call.

        KeySequences are represented as calls to hs.eventtap.keyStroke:
        (ctrl)b+c -> hs.eventtap.keyStroke({"ctrl"}, "b"); hs.eventtap.keyStroke({}, "c");

        Args:
            expr: KeySequence.

        Returns:
            formatted_sequence: str. Formatted hammerspoon eventtap call args.
        """

        combo = expr.combo.accept(self) + ";"

        if expr.key_sequence:
            combo += f" {expr.key_sequence.accept(self)}"

        return combo

    def visit_docstring(self, expr: Docstring) -> str:
        return ""

    def visit_doctag(self, expr: Doctag) -> str:
        return ""
