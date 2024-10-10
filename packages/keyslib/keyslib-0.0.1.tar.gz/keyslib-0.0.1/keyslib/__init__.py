#!/usr/bin/env python3
from keyslib.parser import KeySequence
from keyslib.printer import Printer


def key_sequence(sequence: str) -> KeySequence:
    return KeySequence.from_str(sequence)


def print_key_sequence(key_sequence: KeySequence) -> None:
    Printer().print(key_sequence)
