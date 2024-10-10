#!/usr/bin/env python3
class ParserError(Exception):
    """Error representing any problems encountered during token parsing."""

    pass


class LoaderError(Exception):
    """Error representing any problems encountered while loading a keys file."""


class LoaderDuplicateBindError(Exception):
    """Error representing a duplicate bind encountered in a keys file."""


class LoaderFileNotFoundError(Exception):
    """Error representing a keys file not existing during load."""
