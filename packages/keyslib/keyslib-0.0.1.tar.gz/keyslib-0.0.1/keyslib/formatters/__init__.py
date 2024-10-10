#!/usr/bin/env python3
from typing import Union

from keyslib import KeySequence
from keyslib.printer import Printer

from keyslib.formatters.unicode import UnicodeFormatter, UnicodeHexFormatter
from keyslib.formatters.tmux import TmuxFormatter
from keyslib.formatters.vscode import VSCodeFormatter
from keyslib.formatters.hammerspoon import HammerspoonFormatter

FORMATTERS = {
    "unicode": UnicodeFormatter,
    "unicode_hex": UnicodeHexFormatter,
    "tmux": TmuxFormatter,
    "vscode": VSCodeFormatter,
    "hammerspoon": HammerspoonFormatter,
}


def format_sequence(sequence: Union[str, KeySequence], formatter: str = "print") -> str:
    if isinstance(sequence, str):
        sequence = KeySequence.from_str(sequence)

    if formatter == "print":
        return Printer().to_str(sequence)
    if formatter_cls := FORMATTERS.get(formatter, None):
        return formatter_cls().to_str(sequence)
    else:
        raise ValueError(f"Unknown formatter: {formatter}")
