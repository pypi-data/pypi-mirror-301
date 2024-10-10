#!/usr/bin/env python3
from collections import defaultdict
from typing import Dict, Mapping, Union
from logging import Logger, getLogger

from keyslib import KeySequence

logger: Logger = getLogger(__name__)


_BINDINGS: Dict[str, Dict[str, KeySequence]] = defaultdict(dict)


def bind(
    app: str, name: str, sequence: Union[str, KeySequence], rebind: bool = False
) -> None:
    """Register a keybind.

    Args:
        app: str. Application for keybind, will be stored in binds/<app>.env under
            the keys dir.
        name: str. Name of the binding, usually in ALL_CAPS this will be used
            when referencing the bind in other places.
        sequence: Union[str, KeySequence]. Key sequence to bind.
    """

    if isinstance(sequence, str):
        logger.debug("parsing bind for %s: %s=%s", app, name, sequence)
        sequence = KeySequence.from_str(sequence)

    if not rebind:
        if existing_bind := _BINDINGS[app].get(name, None):
            raise ValueError(
                f"unable to bind {name}, already bound as: {existing_bind}"
            )

    _BINDINGS[app][name] = sequence


def bind_multi(app: str, mappings: Mapping[str, Union[str, KeySequence]]) -> None:
    """Register multiple keybinds.

    Args:
        app: str. Application for keybinds, will be stored in binds/<app>.env under
            the keys dir.
        mappings: Mapping[str, Union[str, KeySequence]]. Mapping of names to
            key sequences to bind.
    """

    for name, sequence in mappings.items():
        bind(app, name, sequence)
