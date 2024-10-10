#!/usr/bin/env python3
from io import StringIO
from collections import defaultdict
from typing import Dict, Iterable
from pathlib import Path
from functools import cache

from dotenv import dotenv_values

from keyslib.exceptions import LoaderFileNotFoundError, LoaderDuplicateBindError
from keyslib.formatters import format_sequence
from keyslib.parser import KeySequence

KeyBinds = Dict[str, Dict[str, KeySequence]]


def parse_binds(binds: Iterable[str]) -> Dict[str, KeySequence]:
    dotenv = dotenv_values(stream=StringIO("\n".join(binds)))
    binds = {}
    for key, value in dotenv.items():
        if not value:
            raise ValueError(f"Unable to parse keybind for {key}")

        binds[key] = KeySequence.from_str(value)

    return binds


def parse_bind(bind: str) -> KeySequence:
    return parse_binds([bind]).popitem()[1]


@cache
def load_binds(app: str, keys_dir: Path = None) -> KeyBinds:
    binds = defaultdict(dict)
    binds_path = keys_dir / "binds" / f"{app}.env"

    if not binds_path.exists():
        raise LoaderFileNotFoundError(f"no keys file file found at path: {binds_path}")

    dotenv = dotenv_values(binds_path)
    for name, sequence_str in dotenv.items():
        if not sequence_str:
            continue

        # Parse in sequence for bind
        sequence = KeySequence.from_str(sequence_str)

        if doc := sequence.doc:
            # Store doc based on doctag group
            group = doc.group
        else:
            # Use default group if no doctag
            group = "default"

        if existing_bind := binds[group].get(name, None):
            raise LoaderDuplicateBindError(
                f"duplicate bind in file for name {name}, already bound as: {existing_bind}"
            )

        binds[group][name] = sequence

    return binds


def get_bind(app: str, group: str, name: str, formatter: str = "print") -> str:
    return format_sequence(load_binds(app)[group][name], formatter)
