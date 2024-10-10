#!/usr/bin/env python3
from pathlib import Path
from typing import Tuple, Iterable
from logging import Logger, getLogger, basicConfig, DEBUG, INFO
from typing import cast, Optional
from os import kill, getenv
from signal import SIGTERM
from time import sleep

import click
from dotenv import set_key
from invoke import run
from invoke.runners import Promise

from keyslib import KeySequence
from keyslib.builder.utils import build_binds
from keyslib.click_param import KeysParam
from keyslib.exceptions import LoaderDuplicateBindError, LoaderFileNotFoundError
from keyslib.formatters import format_sequence
from keyslib.loader import load_binds, parse_bind

from keyslib.cli.context import Context, pass_context


logger: Logger = getLogger(__name__)


def tmux_send_sequence(sequence: str) -> None:
    """Send a key sequence directly to the running tmux session.

    This uses invoke to start a tmux client attached to the session that this is
    running in as a background thread. It then sends the key sequence, followed by
    a detach sequence (ctrl)b+d. This has the effect of sending the keypress to
    the same tmux session keys is running in.

    This should only be used for sending key sequences that control tmux itself,
    such as prefix commands. All other control of applications inside of tmux can
    be done via the "tmux" sender which uses the tmux send-keys command.

    Args:
        sequence: str. KeySequence formatted as unicode.
    """

    # Start a tmux client attached to the session this is running in, enabling
    # pty behavior (since tmux is a manager of ptys), and enabling async, which
    # causes the process to run in a background thread and return a Promise that
    # can be used to interact with it
    # Also supply tmux client flag ignore-size, which allows the client to connect
    # "transparently" without changing the size of the actual client's viewport
    tmux_proc = cast(
        Promise,
        run("tmux attach -f 'ignore-size'", asynchronous=True, pty=True),
    )

    while not tmux_proc.runner.stdout:
        # Busy wait until tmux attaches and returns current stdout
        pass

    # Extra sleep for safety, since initial stdout might still be flowing in
    sleep(0.1)

    # Write key sequence formatted as unicode directly to the stdin of the tmux
    # client in the runner
    tmux_proc.runner.write_proc_stdin(sequence)

    # Write the detach sequence
    tmux_proc.runner.write_proc_stdin(format_sequence("(ctrl)b+d", formatter="unicode"))

    # TODO: This behaves poorly with blocking commands like rename current window,
    # either it joins and completely freezes the actual client, or it is just
    # ignored and the interactive commands silently die off.
    # Join with the background process, which will detach and exit shortly after
    # tmux_proc.join()

    sleep(1)
    try:
        kill(tmux_proc.runner.pid, SIGTERM)
    except ProcessLookupError:
        # Process is probably already gone
        return


def send_sequence(sender: str, sequence: Iterable[KeySequence]) -> None:
    match sender:
        case "wezterm":
            formatter = "unicode"
        case "hammerspoon":
            formatter = "hammerspoon"
        case "tmux":
            formatter = "tmux"
        case "tmux_direct":
            formatter = "unicode"
        case "echo":
            formatter = "print"
        case _:
            click.secho(f"unknown sender: {sender}", fg="red")
            raise click.exceptions.Abort(1)

    for cur_sequence in sequence:
        formatted = format_sequence(cur_sequence, formatter)

        match sender:
            case "wezterm":
                run(f"echo '{formatted}' | wezterm cli send-text --no-paste")
            case "hammerspoon":
                # Without the disown here hs CLI seems to hang, but it doesn't
                # stick around afterwards at least
                run(f"hs -q -c '{formatted}'", pty=False, disown=True)
            case "tmux":
                run(f"tmux send-keys {formatted}")
            case "tmux_direct":
                tmux_send_sequence(formatted)
            case "echo":
                run(f"echo '{formatted}'")
            case _:
                click.secho(f"unknown sender: {sender}", fg="red")
                raise click.exceptions.Abort(1)


def _load_bind(bind: str) -> KeySequence:
    r"""Load a bind selected from keys list --fzf <app> | fzf

    This removes some special formatting applied to improve fzf readability:

    1. Replaces the first tab (\t) delimiter with an equals sign (=)
    2. Splits on the equals sign, yielding the name and key sequence
    3. Replaces the second tab (\t) and doctag (#) with the initial space separated
       one ( #)
    4. Escapes any \ or ' characters in sequence for dotenv's parser
    5. Quotes the sequence and parses it with dotenv

    Args:
        bind: str. Key bind from keys list <app> --fzf and selected by the fzf tool.

    Returns:
        loaded_bind: KeySequence. Loaded key sequence with special formatting
            removed.
    """

    # CMD='(ctrl)b+c #editor Create window' <- CMD=(ctrl)b+c\t#editor Create window
    bind = bind.replace("\t", "=", 1)
    name, sequence = bind.split("=", 1)
    bind = bind.replace("\t#", " #")
    sequence = sequence.replace("'", "\\'").replace("\\", "\\\\")
    bind = f"{name}='{sequence}'"

    return parse_bind(bind)


def _format_bind(name: str, sequence: KeySequence, fzf: bool) -> str:
    r"""Format a bind to be selected from fzf

    This adds some special formatting to improve fzf readability and to reduce
    complexity on the fzf side for speed:
    1. Replace the equals sign (=) with a tab (\t), to be used as a delimiter in
       fzf
    2. Replace the doctag with space ( #) with a tab (\t)

    This should be sent via keys send with the --fzf option, which will reformat
    into the standard key bind format before parsing.

    Args:
        name: str. Bind name.
        sequence: KeySequence. Key sequence for bind.
        fzf: bool. Whether or not to format for fzf.

    Returns:
        formatted_bind: str. Bind formatted with special formatting for fzf.
    """

    if not fzf:
        return f"{name}={sequence}"
    else:
        # name: CMD, sequence: (ctrl)b+c #editor Create window -> CMD\t(ctrl)b+c\t#editor Create window
        str_sequence = str(sequence).replace(" #", "\t#", 1)
        return f"{name}\t{str_sequence}"


@click.group(name="keys", short_help="keys cli")
@click.option(
    "--debug", is_flag=True, default=False, help="Output additional debug info"
)
@click.option(
    "--keys-dir",
    help="The directory to read and store key bindings. Defaults to ~/.config/keyslib",
)
@pass_context
def keys(ctx: Context, debug: bool, keys_dir: Optional[str]) -> None:
    """keys cli

    This tool provides commands for managing "keys files", which are python based
    definitions of keybinds that are then serialized to .env in the standard format
    for use in other tools via custom keybind formatters.

    It also provides commands for sending key sequences to other applications, as
    well as performing interactive keybind completions.
    """

    basicConfig(level=DEBUG if ctx.debug else INFO)

    ctx.debug = debug

    if keys_dir:
        ctx.keys_dir = Path(keys_dir)
    elif xdg_config_home := getenv("XDG_CONFIG_HOME"):
        ctx.keys_dir = Path(xdg_config_home) / "keyslib"


@keys.command(name="format")
@click.argument("formatter", nargs=1, type=str, required=True)
@click.argument("sequence", nargs=-1, type=KeysParam(), required=True)
def keys_format(formatter: str, sequence: Tuple[KeySequence, ...]) -> None:
    """format a key sequence

    Given a formatter and a key sequence(s), this will output the sequence in
    the desired format to stdout, with one on each line.
    """

    for cur_sequence in sequence:
        click.secho(format_sequence(cur_sequence, formatter))


@keys.command("send")
@click.option(
    "--fzf", is_flag=True, default=False, help="handle fzf formatted bind input"
)
@click.argument("sender", nargs=1, type=str, required=True)
@click.argument("sequence", nargs=-1, type=str, required=True)
def keys_send(fzf: bool, sender: str, sequence: Tuple[str, ...]) -> None:
    r"""send a key sequence

    Given a sender and a key sequence(s), this will format and send each key
    sequence to the desired application:

    keys send tmux '(ctrl)w' -> tmux send-keys 'C-w'

    keys send wezterm '(ctrl)b+c' -> echo '\x02c' | wezterm cli send-text --no-paste

    keys send hammerspoon '(alt)1' -> hs -q -c 'hs.eventTap.keyStroke({"alt"}, "1");'

    The --fzf option will consume a bind input that was listed by keys list --fzf
    and selected by the fzf tool.
    """

    if not fzf:
        sequences = [KeySequence.from_str(seq) for seq in sequence]
    else:
        sequences = [_load_bind(seq) for seq in sequence]

    send_sequence(sender, sequences)


@keys.command(name="list")
@click.option("--fzf", is_flag=True, default=False, help="format output for fzf")
@click.argument("app", nargs=1, type=str, required=True)
@click.argument("group", nargs=-1, type=str)
@pass_context
def keys_list(ctx: Context, fzf: bool, app: str, group: Tuple[str, ...]) -> None:
    """list keybinds for an application

    This will load the binds under <app>.env in the keys dir and display them
    in NAME=sequence format.

    Group(s) can be provided to filter the list. By default, all keybinds from
    all groups are listed.

    The --fzf option will format the keys list for selection via the fzf tool.
    """

    try:
        bindings = load_binds(app, ctx.keys_dir)
    except (LoaderFileNotFoundError, LoaderDuplicateBindError) as e:
        click.secho(str(e), fg="red")
        raise click.exceptions.Exit(1)

    if not group:
        list_groups = bindings.keys()
    else:
        list_groups = group

    for cur_group in list_groups:
        if group_bindings := bindings.get(cur_group, None):
            for name, binding in group_bindings.items():
                click.secho(_format_bind(name, binding, fzf))
        else:
            click.secho(f"No group {cur_group} found for app {app}", fg="red")
            raise click.exceptions.Exit(3)


@keys.command(name="get")
@click.argument("app", nargs=1, type=str, required=True)
@click.argument("group", nargs=1, type=str, required=True)
@click.argument("binds", nargs=-1, type=str, required=True)
@pass_context
def keys_get(ctx: Context, app: str, group: str, binds: Tuple[str, ...]) -> None:
    """retrieve a keybind for an application

    Given an app, group, and keybind name(s), this will retrieve the keybinds
    and display them in NAME=sequence format.
    """

    try:
        bindings = load_binds(app, ctx.keys_dir)
    except Exception:
        click.secho(f"No bindings found for app {app}", fg="red")
        raise click.exceptions.Exit(1)

    if group_bindings := bindings.get(group, None):
        for name in binds:
            if binding := group_bindings.get(name, None):
                click.secho(f"{binding}")
            else:
                click.secho(
                    f"No binding found for app {app} with name {name}", fg="red"
                )
                raise click.exceptions.Exit(2)
    else:
        click.secho(f"No group {group} found for app {app}", fg="red")
        raise click.exceptions.Exit(3)


@keys.command(name="build")
@click.option(
    "--keys",
    "_keys",
    type=str,
    help="file or import path to a keys file, defaults to ~/.config/keyslib/keys.py",
    envvar="KEYS_FILE",
)
@pass_context
def keys_build(ctx: Context, _keys: Optional[str]) -> None:
    """build all key files

    This will build the keys.py file under the keys dir (or provided via --keys)
    and write all registered keybinds to their respective binds/<app>.env files.
    These files can then be parsed like any other dotenv file, or using tools
    like fzf.
    """

    if not _keys:
        _keys = ctx.keys_dir / "keys.py"

    build_binds(_keys)

    from keyslib.builder import _BINDINGS

    binds_path = ctx.keys_dir / "binds"

    if not binds_path.exists():
        logger.info(f"creating binds dir at {binds_path}")
        binds_path.mkdir(parents=True)

    for app, bindings in _BINDINGS.items():
        bind_path = binds_path / f"{app}.env"

        # Delete <app>.env if already present, since dotenv will not handle binds
        # that were deleted between builds
        if bind_path.exists():
            bind_path.unlink()

        for name, bind in bindings.items():
            set_key(
                dotenv_path=bind_path,
                key_to_set=name,
                value_to_set=bind.to_str(),
            )


if __name__ == "__main__":
    keys()
