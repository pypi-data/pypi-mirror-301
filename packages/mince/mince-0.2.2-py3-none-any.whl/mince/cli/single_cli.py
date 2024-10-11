"""the single dashboard version
- bypasses the registry
- takes config settings throught arguments
- is meant to be intended within each dashboard package
"""

from __future__ import annotations

import argparse
import importlib

from .. import Dashboard
from . import cli_helpers


subcommands = [
    # 'ls',
    'register',
    'unregister',
    'validate',
    'collect',
    'run',
    'kill',
    'data',
    'spec',
]


def run_single_dashboard_cli(DashboardClass: type[Dashboard]) -> None:
    args = parse_args()

    if args.pdb:
        try:
            args.f_command(args, DashboardClass)
        except Exception:
            cli_helpers._enter_debugger()
    else:
        args.f_command(args, DashboardClass)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=cli_helpers.HelpFormatter)

    # add commands
    subparsers = parser.add_subparsers(dest='command')
    for command in subcommands:
        module_name = 'mince.cli.subcommands.' + command + '_command'
        module = importlib.import_module(module_name)
        arg_adder = getattr(module, 'add_' + command + '_command')
        arg_adder(subparsers, include_dashboard_arg=False)

    # parse args
    args = parser.parse_args()

    if args.command is None:
        import sys

        parser.print_help()
        sys.exit(0)

    return args
