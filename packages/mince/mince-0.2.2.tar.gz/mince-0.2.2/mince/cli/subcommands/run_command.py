from __future__ import annotations

import argparse
import typing

from ... import ops
from .. import cli_helpers

if typing.TYPE_CHECKING:
    from mince import types


def add_run_command(
    subparsers: cli_helpers.Subparsers, include_dashboard_arg: bool
) -> None:
    parser = subparsers.add_parser(
        'run',
        help='run dashboard',
        formatter_class=cli_helpers.HelpFormatter,
    )
    parser.set_defaults(f_command=run_command)
    if include_dashboard_arg:
        parser.add_argument(
            'dashboard',
            help='dashboard to run',
        )
    parser.add_argument(
        '--port',
        help='port number to run dashboard on',
    )
    parser.add_argument(
        '--description',
        help='set description of dashboard',
    )
    parser.add_argument(
        '--no-cache',
        help='do not use data cache',
        action='store_true',
    )
    parser.add_argument(
        '--no-cache-save',
        help='do save data to cache',
        action='store_true',
    )
    parser.add_argument(
        '--no-cache-load',
        help='do load data from cache',
        action='store_true',
    )
    cli_helpers.add_common_args(parser)


def run_command(
    args: argparse.Namespace,
    dashboard: str | typing.Type[types.Dashboard] | None = None,
) -> None:
    registry: types.RegistryFile = {
        'path': args.registry,
        'validate': not args.no_validate,
    }
    if dashboard is None:
        dashboard = args.dashboard
    ops.run_dashboard(
        dashboard=dashboard,
        ui_spec_kwargs={'description': args.description},
        registry=registry,
        run_kwargs={'port': args.port},
        cache=not args.no_cache,
        cache_save=not args.no_cache_save,
        cache_load=not args.no_cache_load,
    )
