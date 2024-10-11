from __future__ import annotations

import importlib
import argparse

from . import cli_helpers


subcommands = [
    'ls',
    'register',
    'unregister',
    'validate',
    'collect',
    'run',
    'kill',
    'data',
    'spec',
    'docker',
]


def run_entire_cli() -> None:
    args = parse_args()

    if args.pdb:
        try:
            args.f_command(args)
        except Exception:
            cli_helpers._enter_debugger()
    else:
        args.f_command(args)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=cli_helpers.HelpFormatter)

    # add commands
    subparsers = parser.add_subparsers(dest='command')
    for command in subcommands:
        module_name = 'mince.cli.subcommands.' + command + '_command'
        module = importlib.import_module(module_name)
        arg_adder = getattr(module, 'add_' + command + '_command')
        arg_adder(subparsers, include_dashboard_arg=True)

    # parse args
    args = parser.parse_args()

    if args.command is None:
        import sys

        parser.print_help()
        sys.exit(0)

    return args
