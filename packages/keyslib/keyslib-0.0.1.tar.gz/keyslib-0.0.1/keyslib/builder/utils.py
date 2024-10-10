#!/usr/bin/env python3
import sys
from importlib.machinery import ModuleSpec
from importlib.util import find_spec, module_from_spec, spec_from_file_location
from os.path import splitext
from pathlib import Path
from logging import Logger, getLogger

from pyre_extensions import none_throws

logger: Logger = getLogger(__name__)


def build_binds(path: str) -> None:
    """Build a keys file.

    Given a path to a keys.py file, or a module path, this will load and execute
    the path, which will be used to build all key bindings files.

    Args:
        path: str. Either a python module path or a file path to a keys file.

    Raises:
        ValueError: If a key module or file exists, but yields no valid module
            spec.
    """

    if splitext(path)[1] == ".py":
        # Path is (probably) a file, attempt to load a spec at this path.
        module_spec = spec_from_file_location("keys", path)
    else:
        # Path is a module path, attempt to find a spec in the class path.
        module_spec = find_spec(path)

    if not isinstance(module_spec, ModuleSpec):
        # File/module exists, but yielded no spec on load.
        raise ValueError(f"could not locate root tome module at {path}")

    # Make the path that the keys file is present in the first python path,
    # allowing for "local" imports.
    module_path = Path(none_throws(module_spec.origin)).parent
    if sys.path[0] != module_path:
        sys.path.insert(0, str(module_path))

    # Load and execute the keys module.
    module = module_from_spec(module_spec)
    none_throws(module_spec.loader).exec_module(module)
