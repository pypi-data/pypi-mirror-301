#!/usr/bin/env python3
from testslide import TestCase

from keyslib.scanner import TokenType, Token, Scanner
from keyslib.types import ModifierType, KeywordType

EOF = Token(type=TokenType.EOF)


class KeysScannerTests(TestCase):
    def test_primary(self) -> None:
        self.assertEqual(
            Scanner.scan("b"), [Token(type=TokenType.PRIMARY, value="b"), EOF]
        )

    def test_keyword(self) -> None:
        self.assertEqual(
            Scanner.scan("<left>"),
            [
                Token(type=TokenType.LESS_THAN),
                Token(type=TokenType.KEYWORD, value=KeywordType.LEFT),
                Token(type=TokenType.GREATER_THAN),
                EOF,
            ],
        )

    def test_modifier(self) -> None:
        self.assertEqual(
            Scanner.scan("ctrl"),
            [Token(type=TokenType.MODIFIER, value=ModifierType.CTRL), EOF],
        )

    def test_mask(self) -> None:
        self.assertEqual(
            Scanner.scan("ctrl|alt"),
            [
                Token(type=TokenType.MODIFIER, value=ModifierType.CTRL),
                Token(type=TokenType.PIPE),
                Token(type=TokenType.MODIFIER, value=ModifierType.ALT),
                EOF,
            ],
        )

    def test_combo(self) -> None:
        self.assertEqual(
            Scanner.scan("(ctrl|alt)b"),
            [
                Token(type=TokenType.LEFT_PAREN),
                Token(type=TokenType.MODIFIER, value=ModifierType.CTRL),
                Token(type=TokenType.PIPE),
                Token(type=TokenType.MODIFIER, value=ModifierType.ALT),
                Token(type=TokenType.RIGHT_PAREN),
                Token(type=TokenType.PRIMARY, value="b"),
                EOF,
            ],
        )

    def test_key_sequence(self) -> None:
        self.assertEqual(
            Scanner.scan("( ctrl |  alt )  b  + (cmd)<left>"),
            [
                Token(type=TokenType.LEFT_PAREN),
                Token(type=TokenType.MODIFIER, value=ModifierType.CTRL),
                Token(type=TokenType.PIPE),
                Token(type=TokenType.MODIFIER, value=ModifierType.ALT),
                Token(type=TokenType.RIGHT_PAREN),
                Token(type=TokenType.PRIMARY, value="b"),
                Token(type=TokenType.PLUS),
                Token(type=TokenType.LEFT_PAREN),
                Token(type=TokenType.MODIFIER, value=ModifierType.CMD),
                Token(type=TokenType.RIGHT_PAREN),
                Token(type=TokenType.LESS_THAN),
                Token(type=TokenType.KEYWORD, value=KeywordType.LEFT),
                Token(type=TokenType.GREATER_THAN),
                EOF,
            ],
        )

    def test_docstring(self) -> None:
        self.assertEqual(
            Scanner.scan("(ctrl)b+c # create a <window"),
            [
                Token(type=TokenType.LEFT_PAREN),
                Token(type=TokenType.MODIFIER, value=ModifierType.CTRL),
                Token(type=TokenType.RIGHT_PAREN),
                Token(type=TokenType.PRIMARY, value="b"),
                Token(type=TokenType.PLUS),
                Token(type=TokenType.PRIMARY, value="c"),
                Token(type=TokenType.DOCSTRING, value=" create a <window"),
                EOF,
            ],
        )
