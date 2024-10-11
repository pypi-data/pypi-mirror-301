from __future__ import annotations

import argparse
import typing

from ... import ops
from .. import cli_helpers

if typing.TYPE_CHECKING:
    from mince import types


def add_data_command(
    subparsers: cli_helpers.Subparsers, include_dashboard_arg: bool
) -> None:
    parser = subparsers.add_parser(
        'data',
        help='view dashboard data',
        formatter_class=cli_helpers.HelpFormatter,
    )
    parser.set_defaults(f_command=data_command)
    if include_dashboard_arg:
        parser.add_argument(
            'dashboard',
            help='dashboard to get data of',
        )
    parser.add_argument(
        '-i',
        '--interactive',
        help='load data in interactive python session',
        action='store_true',
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


def data_command(
    args: argparse.Namespace,
    dashboard: str | typing.Type[types.Dashboard] | None = None,
) -> None:
    registry: types.RegistryFile = {
        'path': args.registry,
        'validate': not args.no_validate,
    }
    if dashboard is None:
        dashboard = args.dashboard
    data = ops.load_dashboard_data(
        dashboard=dashboard,
        registry=registry,
        cache=not args.no_cache,
        cache_save=not args.no_cache_save,
        cache_load=not args.no_cache_load,
    )

    if args.interactive:
        cli_helpers.open_interactive_session(variables=data)
    else:
        first = True
        for key, df in data.items():
            print()
            if first:
                first = False
            else:
                print()
            print('name =', key)
            print(df)
