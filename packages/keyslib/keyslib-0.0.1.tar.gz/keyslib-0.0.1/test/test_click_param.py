#!/usr/bin/env python3
from testslide import TestCase

import click
from click.testing import CliRunner

from keyslib import KeySequence
from keyslib.click_param import KeysParam


class KeysClickParamTests(TestCase):
    def test_click_param(self) -> None:
        expected_keys: str = "(ctrl|alt)<left>+(shift|cmd)b"
        expected_key_sequence: KeySequence = KeySequence(expected_keys)

        @click.command("test")
        @click.argument("keys", nargs=1, type=KeysParam(), required=True)
        def test(keys: KeySequence) -> None:
            if keys != expected_key_sequence:
                raise click.exceptions.Exit(1)

        result = CliRunner().invoke(test, [expected_keys])
        self.assertEqual(result.exit_code, 0)
