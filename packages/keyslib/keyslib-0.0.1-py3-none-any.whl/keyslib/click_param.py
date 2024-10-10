#!/usr/bin/env python3
from typing import Any, Optional

from click import Context, Parameter, ParamType

from keyslib import KeySequence


class KeysParam(ParamType):
    """Click parameter type for a key sequence.

    Example Usage:
    @click.command(name="foobar")
    @click.argument("keys", nargs=1, type=KeysParam(), required=True)
    def cli(keys: KeySequence) -> None:
        print(keys.combo.key)
        print(keys.combo.mask)

    foobar "(ctrl|alt)c"
    (ctrl|alt)
    c
    """

    name = "keys"

    def convert(
        self,
        # Any matches the override
        # pyre-ignore[2]: Parameter `value` must have a type other than `Any`.
        value: Optional[Any],
        param: Optional[Parameter],
        ctx: Optional[Context],
    ) -> KeySequence:
        if isinstance(value, str):
            try:
                return KeySequence.from_str(value)
            except Exception as e:
                self.fail(str(e))
        else:
            self.fail("Key sequence must be a string")
