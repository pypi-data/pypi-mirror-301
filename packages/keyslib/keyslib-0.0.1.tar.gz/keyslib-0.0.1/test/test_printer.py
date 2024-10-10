#!/usr/bin/env python3
from testslide import TestCase

from keyslib.parser import (
    Primary,
    Keyword,
    Modifier,
    Mask,
    Combo,
    Key,
    KeySequence,
)
from keyslib.printer import Printer
from keyslib.types import KeywordType, ModifierType


class KeysPrinterTests(TestCase):
    def setUp(self) -> None:
        self.printer = Printer()

    def test_primary(self) -> None:
        self.assertEqual(self.printer.to_str(Primary(value="b")), "b")

    def test_keyword(self) -> None:
        self.assertEqual(self.printer.to_str(Keyword(value=KeywordType.LEFT)), "<left>")

    def test_modifier(self) -> None:
        self.assertEqual(self.printer.to_str(Modifier(value=ModifierType.CTRL)), "ctrl")

    def test_mask(self) -> None:
        mask = Mask(
            modifier=Modifier(value=ModifierType.CTRL),
            mask=Mask(modifier=Modifier(value=ModifierType.ALT)),
        )

        self.assertEqual(self.printer.to_str(mask), "ctrl|alt")

    def test_combo(self) -> None:
        combo = Combo(
            key=Key(value=Keyword(value=KeywordType.LEFT)),
            mask=Mask(
                modifier=Modifier(value=ModifierType.CTRL),
                mask=Mask(modifier=Modifier(value=ModifierType.ALT)),
            ),
        )

        self.assertEqual(self.printer.to_str(combo), "(ctrl|alt)<left>")

    def test_key_sequence(self) -> None:
        key_sequence = KeySequence(
            combo=Combo(
                key=Key(value=Keyword(value=KeywordType.LEFT)),
                mask=Mask(
                    modifier=Modifier(value=ModifierType.CTRL),
                    mask=Mask(modifier=Modifier(value=ModifierType.ALT)),
                ),
            ),
            key_sequence=KeySequence(
                combo=Combo(
                    key=Key(value=Primary(value="b")),
                    mask=Mask(
                        modifier=Modifier(value=ModifierType.CMD),
                        mask=Mask(modifier=Modifier(value=ModifierType.SHIFT)),
                    ),
                ),
            ),
        )

        self.assertEqual(
            self.printer.to_str(key_sequence), "(ctrl|alt)<left>+(cmd|shift)b"
        )
