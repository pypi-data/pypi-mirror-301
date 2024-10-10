#!/usr/bin/env python3
from enum import auto, IntEnum


class KeywordType(IntEnum):
    """Keywords/named keys

    These translate to normal characters for keys that use reserved names:
    <left> -> KeywordType.LEFT

    Not all keywords are supported in all formatters.
    """

    UNKNOWN = 0

    # Arrow keys
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()

    # Special keys
    SPACE = auto()
    BACKSPACE = auto()
    TAB = auto()
    DELETE = auto()
    ENTER = auto()
    ESCAPE = auto()
    END = auto()
    HOME = auto()
    INSERT = auto()
    PAGEDOWN = auto()
    PAGEUP = auto()
    CAPSLOCK = auto()
    BREAK = auto()

    # Function keys
    F1 = auto()
    F2 = auto()
    F3 = auto()
    F4 = auto()
    F5 = auto()
    F6 = auto()
    F7 = auto()
    F8 = auto()
    F9 = auto()
    F10 = auto()
    F11 = auto()
    F12 = auto()

    # Numpad keys
    NUMPAD0 = auto()
    NUMPAD1 = auto()
    NUMPAD2 = auto()
    NUMPAD3 = auto()
    NUMPAD4 = auto()
    NUMPAD5 = auto()
    NUMPAD6 = auto()
    NUMPAD7 = auto()
    NUMPAD8 = auto()
    NUMPAD9 = auto()
    NUMPADMUL = auto()
    NUMPADADD = auto()
    NUMPADSEP = auto()
    NUMPADSUB = auto()
    NUMPADDEC = auto()
    NUMPADDIV = auto()

    LPAREN = auto()
    RPAREN = auto()
    PLUS = auto()
    MUL = auto()
    QUOTE = auto()
    PIPE = auto()
    LESSTHAN = auto()
    GREATERTHAN = auto()
    HASH = auto()


class ModifierType(IntEnum):
    """Modifier keys

    These translate to a mask that is applied to the key that they modify:
    (ctrl|alt)b -> (ModifierType.CTRL / ModifierType.ALT) * Key("b")

    Not all modifiers and masks are available in all formatters. For example,
    the shift modifier does not apply to text based formatters like tmux and
    unicode as they just use literal chars instead, ie P instead of (shift)p
    """

    UNKNOWN = 0
    CTRL = auto()
    ALT = auto()
    CMD = auto()
    SHIFT = auto()
    FN = auto()
