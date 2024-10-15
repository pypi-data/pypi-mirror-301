from __future__ import annotations

import importlib
import argparse

from . import cli_helpers


def parse_args(
    subcommands: list[str], include_dashboard_arg: bool
) -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=cli_helpers.HelpFormatter)

    # add commands
    subparsers = parser.add_subparsers(dest='command')
    for command in subcommands:
        module_name = 'mince.cli.subcommands.' + command + '_command'
        module = importlib.import_module(module_name)
        arg_adder = getattr(module, 'add_' + command + '_command')
        arg_adder(subparsers, include_dashboard_arg=include_dashboard_arg)

    # parse args
    args = parser.parse_args()

    if args.command is None:
        import sys

        parser.print_help()
        sys.exit(0)

    return args


def add_common_args(
    parser: argparse.ArgumentParser, registry_name: str = '--registry'
) -> None:
    parser.add_argument(
        registry_name,
        metavar='PATH',
        help='path to mince registry',
    )
    parser.add_argument(
        '--no-validate',
        help='skip validation of registry',
        action='store_true',
    )
    parser.add_argument(
        '--debug',
        help='use debug mode',
        action='store_true',
    )
    parser.add_argument(
        '--pdb',
        help='use interactive debugger',
        action='store_true',
    )
