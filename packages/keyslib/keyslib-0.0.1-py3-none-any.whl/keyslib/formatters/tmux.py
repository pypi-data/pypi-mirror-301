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

from keyslib.types import ModifierType, KeywordType
from keyslib.visitor import Visitor


class TmuxFormatter(Visitor):
    """tmux formatter for key sequences.

    This will format a KeySequence for use in tmux bindings as well as the tmux
    "send-keys" command:

    (ctrl|alt)c     -> C-M-c
    (shift)<insert> -> S-IC

    Keys with multiple-modifier masks are bind only and do not work with send-keys.

    Reference: https://man.archlinux.org/man/tmux.1#KEY_BINDINGS
    """

    def to_str(self, expr: Expr) -> str:
        return expr.accept(self)

    def print(self, expr: Expr) -> None:
        print(self.to_str(expr))

    def accept(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_primary(self, expr: Primary) -> str:
        """Format a Primary for a tmux key expression.

        Primary chars are used directly by value in tmux.

        Args:
            expr: Primary. Primary for a Key to be formatted.

        Returns:
            formatted_primary: Primary char formatted for use in a tmux key
                expression.
        """

        return expr.value

    def visit_keyword(self, expr: Keyword) -> str:
        """Format a Keyword for a tmux key expression.

        A subset of available keywords is defined in the tmux man page and are
        translated to their tmux keyword equivalents:
        (ctrl)<backspace> -> C-BSpace

        Args:
            expr: Keyword. Keyword for a Key to be formatted.

        Returns:
            formatted_keyword: Keyword formatted for use in a tmux key expression.
        """

        # TODO: A command bound to the Any key will execute for all keys which
        # do not have a more specific binding. This is a tmux only keyword that
        # should be allowed somehow. Possibly adding support for arbitrary strings
        # of text in quotes?

        # tmux keyword translation:
        # https://man.archlinux.org/man/tmux.1#KEY_BINDINGS
        match expr.value:
            case KeywordType.UP:
                return "Up"
            case KeywordType.DOWN:
                return "Down"
            case KeywordType.LEFT:
                return "Left"
            case KeywordType.RIGHT:
                return "Right"
            case KeywordType.SPACE:
                return "Space"
            case KeywordType.BACKSPACE:
                return "BSpace"
            case KeywordType.TAB:
                return "Tab"
            case KeywordType.DELETE:
                return "DC"
            case KeywordType.ENTER:
                return "Enter"
            case KeywordType.ESCAPE:
                return "Escape"
            case KeywordType.END:
                return "End"
            case KeywordType.HOME:
                return "Home"
            case KeywordType.INSERT:
                return "IC"
            case KeywordType.PAGEDOWN:
                return "PgDn"
            case KeywordType.PAGEUP:
                return "PgUp"
            case KeywordType.F1:
                return "F1"
            case KeywordType.F2:
                return "F2"
            case KeywordType.F3:
                return "F3"
            case KeywordType.F4:
                return "F4"
            case KeywordType.F5:
                return "F5"
            case KeywordType.F6:
                return "F6"
            case KeywordType.F7:
                return "F7"
            case KeywordType.F8:
                return "F8"
            case KeywordType.F9:
                return "F9"
            case KeywordType.F10:
                return "F10"
            case KeywordType.F11:
                return "F11"
            case KeywordType.F12:
                return "F12"
            case KeywordType.LPAREN:
                return "\("
            case KeywordType.RPAREN:
                return "\)"
            case KeywordType.PLUS:
                return "+"
            case KeywordType.MUL:
                return "\*"
            case KeywordType.QUOTE:
                return '"'
            case KeywordType.PIPE:
                return "\|"
            case KeywordType.LESSTHAN:
                return "\<"
            case KeywordType.GREATERTHAN:
                return "\>"
            case KeywordType.HASH:
                return "\#"
            case _:
                raise ValueError(f"Unsupported tmux keyword: {expr}")

    def visit_modifier(self, expr: Modifier) -> str:
        """Format a Modifier for a tmux key expression.

        Only the ctrl/alt/shift modifiers are supported, as tmux has no handling
        for CMD in general.

        (ctrl)b -> C-b
        (alt)b -> M-b
        (shift)b -> S-b

        The shift modifier is bind only. For send-keys, just use the literal
        shifted char instead ie : instead of (shift);

        Args:
            expr: Modifier. Modifier for a Mask to be formatted.

        Returns:
            formatted_modifier: Modifier formatted for a tmux key expression mask.
        """

        # tmux modifier translation:
        # https://man.archlinux.org/man/tmux.1#KEY_BINDINGS
        match expr.value:
            case ModifierType.CTRL:
                return "C"
            case ModifierType.ALT:
                return "M"
            case ModifierType.SHIFT:
                # NOTE: The shift modifier is bind only and is unsupported
                # in send-keys
                return "S"
            case _:
                raise ValueError(f"Unsupported tmux modifier: {expr}")

    def visit_mask(self, expr: Mask) -> str:
        """Format a Mask for a tmux key expression.

        Masks in tmux are expressed as a dash separated set of modifiers:
        (ctrl|alt)b -> C-M-b

        There is one special case, (shift)<tab> which is expressed as BTab instead
        of S-Tab.

        Args:
            expr: Mask from a Combo to be formatted.

        Returns:
            formatted_mask: str. Mask formattted for a tmux key expression.
        """

        modifiers = expr.modifier.accept(self) + "-"

        if expr.mask:
            # NOTE: Multiple masks (ie (ctrl|alt)c -> C-M-c) are bind only, and
            # are unsupported in send-keys
            modifiers += expr.mask.accept(self)

        if modifiers == "S-Tab":
            # tmux uses it's own "keyword" BTab to represent a Shift+Tab
            # sequence
            modifiers = "BTab"

        return modifiers

    def visit_combo(self, expr: Combo) -> str:
        """Format a Combo as a tmux key expression.

        A Combo in tmux is expressed as a dash separated mask and primary char,
        with tmux specific substitutions for supported keywords:
        (ctrl)b -> C-b
        (alt|shift)P -> M-S-P
        """

        if expr.mask:
            mask = expr.mask.accept(self)
        else:
            mask = ""

        return f"{mask + expr.key.accept(self)}"

    def visit_key_sequence(self, expr: KeySequence) -> str:
        """Format a KeySequence as a tmux key expression.

        This will format a KeySequence for use in tmux bindings as well as the tmux
        "send-keys" command:
        (ctrl|alt)b+c -> C-M-b c
        (shift)<insert> -> S-IC

        Args:
            expr: KeySequence.

        Returns:
            formatted_sequence: str. Formatted tmux key sequence expression.
        """

        combo = expr.combo.accept(self)

        if expr.key_sequence:
            combo += f" {expr.key_sequence.accept(self)}"

        return combo

    def visit_docstring(self, expr: Docstring) -> str:
        return ""

    def visit_doctag(self, expr: Doctag) -> str:
        return ""
