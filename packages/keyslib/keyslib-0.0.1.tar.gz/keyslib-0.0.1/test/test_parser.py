#!/usr/bin/env python3
from testslide import TestCase

from keyslib.parser import (
    Primary,
    Keyword,
    Key,
    Modifier,
    Mask,
    Combo,
    KeySequence,
)
from keyslib.types import ModifierType, KeywordType


class KeysParserTests(TestCase):
    def test_primary(self) -> None:
        expected_primary = Primary(value="b")

        self.assertEqual(Primary("b"), expected_primary)

    def test_keyword(self) -> None:
        expected_keyword = Keyword(value=KeywordType.LEFT)

        self.assertEqual(Keyword("<left>"), expected_keyword)

    def test_key(self) -> None:
        expected_key_keyword = Key(value=Keyword(value=KeywordType.LEFT))

        self.assertEqual(Key("<left>"), expected_key_keyword)

        expected_key_primary = Key(value=Primary(value="b"))

        self.assertEqual(Key("b"), expected_key_primary)

    def test_modifier(self) -> None:
        expected_modifier = Modifier(value=ModifierType.CTRL)

        self.assertEqual(Modifier("ctrl"), expected_modifier)

    def test_mask(self) -> None:
        expected_mask = (
            Mask(modifier=Modifier(value=ModifierType.ALT))
            / Mask(modifier=Modifier(value=ModifierType.CTRL))
            / Mask(modifier=Modifier(value=ModifierType.SHIFT))
            / Mask(modifier=Modifier(value=ModifierType.CMD))
        )

        self.assertEqual(Mask("alt|ctrl|shift|cmd"), expected_mask)

        self.assertEqual(Mask("alt") / "ctrl" / "shift" / "cmd", expected_mask)

    def test_combo(self) -> None:
        expected_combo = Combo(
            key=Key("<left>"),
            mask=Mask("ctrl|alt"),
        )

        self.assertEqual(Combo("(ctrl|alt)<left>"), expected_combo)

        self.assertEqual((Mask("ctrl") / "alt") * Combo("<left>"), expected_combo)

    def test_key_sequence(self) -> None:
        expected_key_sequence = KeySequence(
            combo=Combo(
                "(ctrl|shift|alt|cmd)b",
            ),
            key_sequence=KeySequence(
                combo=Combo("(ctrl)<left>"),
                key_sequence=KeySequence(combo=Combo("(cmd|alt)c")),
            ),
        )

        self.assertEqual(
            KeySequence("(ctrl|shift|alt|cmd)b+(ctrl)<left>+(cmd|alt)c"),
            expected_key_sequence,
        )

        self.assertEqual(
            KeySequence("(ctrl|shift|alt|cmd)b") + "(ctrl)<left>" + "(cmd|alt)c",
            expected_key_sequence,
        )
