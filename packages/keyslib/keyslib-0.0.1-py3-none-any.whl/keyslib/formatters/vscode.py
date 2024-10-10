#!/usr/bin/env python3
from __future__ import annotations

from typing import Set, Dict

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


class VSCodeFormatter(Visitor):
    """VSCode formatter for key sequences.

    This will format a KeySequence for use in the "key" field of a keybinding
    in VSCode's keybindings.json file:

    (alt)P+(ctrl|shift)<enter> -> "alt+shift+p ctrl+shift+enter"

    Reference: https://code.visualstudio.com/docs/getstarted/keybindings#_keyboard-rules
    """

    # Allowed non-alphanumeric primary key chars
    # https://code.visualstudio.com/docs/getstarted/keybindings#_keyboard-rules
    ALLOWED_SPECIAL_CHARS: Set[str] = {
        "`",
        "-",
        "=",
        "[",
        "]",
        "\\",
        ";",
        "'",
        ",",
        ".",
        "/",
    }

    # Mapping of "shifted" primary chars to their unshifted char equivalents
    CONVERTIBLE_CHARS: Dict[str, str] = {
        "!": "1",
        "@": "2",
        "$": "4",
        "%": "5",
        "^": "6",
        "&": "7",
        "_": "-",
        "{": "[",
        "}": "]",
        ":": ";",
        "?": "/",
    }

    # Mapping of "shifted" keywords to their unshifted char equivalents
    CONVERTIBLE_KEYWORDS: Dict[KeywordType, str] = {
        KeywordType.LPAREN: "9",
        KeywordType.RPAREN: "0",
        KeywordType.PLUS: "=",
        KeywordType.MUL: "8",
        KeywordType.QUOTE: ",",
        KeywordType.PIPE: "\\",
        KeywordType.LESSTHAN: ",",
        KeywordType.GREATERTHAN: ".",
        KeywordType.HASH: "3",
    }

    def to_str(self, expr: Expr) -> str:
        return expr.accept(self)

    def print(self, expr: Expr) -> None:
        print(self.to_str(expr))

    def accept(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_primary(self, expr: Primary) -> str:
        """Format a Primary for a VSCode keybind.

        A subset of primary chars can be directly specified, and is defined under
        "Accepted Keys" in the VSCode keybindings reference. In particular, all
        shifted characters must instead be converted to their unshifted equivalent
        with a shift mask applied ie:
        (alt)P -> "alt+shift+p"

        This is mostly handled in the Combo formatter since a mask has to be
        conditionally applied based on the character value.

        Args:
            expr: Primary. Primary for a Key to be formatted.

        Returns:
            formatted_primary: Primary char formatted for use in a VSCode keybind.
        """

        if (
            not expr.value.isalnum()
            and expr.value not in self.ALLOWED_SPECIAL_CHARS
            and expr.value not in self.CONVERTIBLE_CHARS
        ):
            raise ValueError(
                f"Unsupported special char for vscode, allowed chars are: {self.ALLOWED_SPECIAL_CHARS}"
            )

        return expr.value

    def visit_keyword(self, expr: Keyword) -> str:
        """Format a Keyword for a VSCode keybind.

        A subset of available keywords is defined under "Accepted Keys" in the
        VSCode keybindings reference:
        (ctrl)<numpadmul> -> ctrl+numpad_multiply

        Args:
            expr: Keyword. Keyword for a Key to be formatted.

        Returns:
            formatted_keyword: Keyword formatted for use in a VSCode keybind.
        """

        # vscode keyword translation:
        # https://code.visualstudio.com/docs/getstarted/keybindings#_keyboard-rules
        match expr.value:
            case KeywordType.UP:
                return "up"
            case KeywordType.DOWN:
                return "down"
            case KeywordType.LEFT:
                return "left"
            case KeywordType.RIGHT:
                return "right"
            case KeywordType.SPACE:
                return "space"
            case KeywordType.BACKSPACE:
                return "backspace"
            case KeywordType.TAB:
                return "tab"
            case KeywordType.DELETE:
                return "delete"
            case KeywordType.ENTER:
                return "enter"
            case KeywordType.ESCAPE:
                return "escape"
            case KeywordType.END:
                return "end"
            case KeywordType.HOME:
                return "home"
            case KeywordType.INSERT:
                return "insert"
            case KeywordType.PAGEDOWN:
                return "pagedown"
            case KeywordType.PAGEUP:
                return "pageup"
            case KeywordType.CAPSLOCK:
                return "capslock"
            case KeywordType.BREAK:
                return "pausebreak"
            case KeywordType.F1:
                return "f1"
            case KeywordType.F2:
                return "f2"
            case KeywordType.F3:
                return "f3"
            case KeywordType.F4:
                return "f4"
            case KeywordType.F5:
                return "f5"
            case KeywordType.F6:
                return "f6"
            case KeywordType.F7:
                return "f7"
            case KeywordType.F8:
                return "f8"
            case KeywordType.F9:
                return "f9"
            case KeywordType.F10:
                return "f10"
            case KeywordType.F11:
                return "f11"
            case KeywordType.F12:
                return "f12"
            case KeywordType.NUMPAD0:
                return "numpad0"
            case KeywordType.NUMPAD1:
                return "numpad1"
            case KeywordType.NUMPAD2:
                return "numpad2"
            case KeywordType.NUMPAD3:
                return "numpad3"
            case KeywordType.NUMPAD4:
                return "numpad4"
            case KeywordType.NUMPAD5:
                return "numpad5"
            case KeywordType.NUMPAD6:
                return "numpad6"
            case KeywordType.NUMPAD7:
                return "numpad7"
            case KeywordType.NUMPAD8:
                return "numpad8"
            case KeywordType.NUMPAD9:
                return "numpad9"
            case KeywordType.NUMPADMUL:
                return "numpad_multiply"
            case KeywordType.NUMPADADD:
                return "numpad_add"
            case KeywordType.NUMPADSEP:
                return "numpad_separator"
            case KeywordType.NUMPADSUB:
                return "numpad_subtract"
            case KeywordType.NUMPADDEC:
                return "numpad_decimal"
            case KeywordType.NUMPADDIV:
                return "numpad_divide"
            case _:
                raise ValueError(f"Unsupported vscode keyword: {expr}")

    def visit_modifier(self, expr: Modifier) -> str:
        """Format a Modifier for a VSCode keybind.

        Modifiers translate directly by name.

        Args:
            expr: Modifier. Modifier for a Mask to be formatted.

        Returns:
            formatted_modifier: Modifier formatted for use in a VSCode keybind.
        """

        # vscode modifier translation:
        # https://code.visualstudio.com/docs/getstarted/keybindings#_keyboard-rules
        match expr.value:
            case ModifierType.CTRL:
                return "ctrl"
            case ModifierType.ALT:
                return "alt"
            case ModifierType.SHIFT:
                return "shift"
            case ModifierType.CMD:
                return "cmd"
            case _:
                raise ValueError(f"Unsupported vscode modifier: {expr}")

    def visit_mask(self, expr: Mask) -> str:
        """Format a Mask for a VSCode keybind.

        Masks in VSCode are just expressed as a plus-separated set of modifiers:
        (ctrl|alt|shift|cmd)p -> ctrl+alt+shift+cmd+p

        Args:
            expr: Mask from a Combo to be formatted.

        Returns:
            formatted_mask: str. Mask formattted for use in a VSCode keybind.
        """

        modifiers = expr.modifier.accept(self) + "+"

        if expr.mask:
            modifiers += expr.mask.accept(self)

        return modifiers

    def visit_combo(self, expr: Combo) -> str:
        """Format a Combo for a VSCode keybind.

        Mainly, this handles a VSCode quirk where any uppercase/shifted primary
        chars and keywords are expressed as "shift+primary", where primary is the
        equivalent "lowercase"/unshifted char ie:
        (alt)P -> "alt+shift+p"

        Args:
            expr: Combo. Combo from a KeySequence to be formatted.

        Returns:
            formatted_combo: str. Combo formatted for use in a VSCode keybind.
        """

        if expr.mask:
            mask = expr.mask.accept(self)
        else:
            mask = ""

        key = expr.key

        if isinstance(key.value, Primary) and key.value.value.isupper():
            # All uppercase letters are expressed in vscode as shift+<l>
            # (alt)P -> alt+shift+p
            key = key.value.value.lower()
            mask += "shift+"
        elif (
            isinstance(key.value, Primary) and key.value.value in self.CONVERTIBLE_CHARS
        ):
            # The same is true for special chars as well
            # (alt)% -> alt+shift+5
            key = self.CONVERTIBLE_CHARS[key.value.value]
            mask += "shift+"
        elif (
            isinstance(key.value, Keyword)
            and key.value.value in self.CONVERTIBLE_KEYWORDS
        ):
            # Handle shift for keywords
            # (alt)<lparen> -> alt+shift+9
            key = self.CONVERTIBLE_KEYWORDS[key.value.value]
            mask += "shift+"
        else:
            # Handle key as normal
            key = key.accept(self)

        return mask + key

    def visit_key_sequence(self, expr: KeySequence) -> str:
        """Format a KeySequence as a VSCode keybind.

        This will format a KeySequence for use in the "key" field of a keybinding
        in VSCode's keybindings.json file.

        (alt)P+(ctrl|shift)<enter> -> "alt+shift+p ctrl+shift+enter"

        Args:
            expr: KeySequence.

        Returns:
            formatted_sequence: str. Sequence formatted for use in VSCode keybind.
        """

        combo = expr.combo.accept(self)

        if expr.key_sequence:
            # From https://code.visualstudio.com/docs/getstarted/keybindings#_keyboard-rules
            # Chords (two separate keypress actions) are described by separating the
            # two keypresses with a space. For example, Ctrl+K Ctrl+C.
            combo += f" {expr.key_sequence.accept(self)}"

        return combo

    def visit_docstring(self, expr: Docstring) -> str:
        return ""

    def visit_doctag(self, expr: Doctag) -> str:
        return ""
