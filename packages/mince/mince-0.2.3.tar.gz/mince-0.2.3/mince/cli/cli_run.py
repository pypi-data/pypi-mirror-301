from __future__ import annotations

from mince import Dashboard
from . import cli_parsing
from . import cli_helpers


def run_entire_cli() -> None:
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

    args = cli_parsing.parse_args(
        subcommands=subcommands,
        include_dashboard_arg=True,
    )

    if args.pdb:
        try:
            args.f_command(args)
        except Exception:
            cli_helpers._enter_debugger()
    else:
        args.f_command(args)


def run_single_dashboard_cli(DashboardClass: type[Dashboard]) -> None:
    subcommands = [
        'register',
        'unregister',
        'validate',
        'collect',
        'run',
        'kill',
        'data',
        'spec',
    ]

    args = cli_parsing.parse_args(
        subcommands=subcommands,
        include_dashboard_arg=False,
    )

    if args.pdb:
        try:
            args.f_command(args, DashboardClass)
        except Exception:
            cli_helpers._enter_debugger()
    else:
        args.f_command(args, DashboardClass)
