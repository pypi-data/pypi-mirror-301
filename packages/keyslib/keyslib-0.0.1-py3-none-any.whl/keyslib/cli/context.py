#!/usr/bin/env python3
from pathlib import Path
from typing import Callable, Any

from click import make_pass_decorator


class Context:
    """
    Click CLI context class.

    This class is used to share data from the Click CLI throughout the keys cli.

    Attributes:
        debug: bool. Run in debug mode, causing additional output and diagnostics.
        keys_dir: Path. Path to load and store keyslib cli configuration, defaults
            to ~/.config/keyslib
    """

    def __init__(self) -> None:
        """Initialize a Click CLI context."""

        self.debug = False
        self.keys_dir = Path.home() / ".config/keyslib"


# Function decorator to pass global CLI context into a function.
# pyre-fixme[5]: Globally accessible variable `pass_context` must be specified
# as type that does not contain `Any`.
pass_context: Callable[..., Any] = make_pass_decorator(Context, ensure=True)
