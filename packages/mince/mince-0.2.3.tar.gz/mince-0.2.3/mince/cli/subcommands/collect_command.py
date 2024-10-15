from __future__ import annotations

import argparse
import typing

from ... import ops
from .. import cli_helpers
from .. import cli_parsing

if typing.TYPE_CHECKING:
    from mince import types


def add_collect_command(
    subparsers: cli_helpers.Subparsers, include_dashboard_arg: bool
) -> None:
    parser = subparsers.add_parser(
        'collect',
        help='collect data of dashboard',
        formatter_class=cli_helpers.HelpFormatter,
    )
    parser.add_argument(
        '--intervals',
        nargs='+',
        metavar='INTERVAL',
        help='intervals to collect: {day week month}',
    )
    parser.add_argument(
        '--recollect',
        help='recollect existing files instead of skipping',
        action='store_true',
    )
    parser.add_argument(
        '--skip-incomplete-intervals',
        help='skip incomplete time intervals instead of collecting them',
        action='store_true',
    )
    parser.add_argument(
        '--start-date',
        help='start date to use [default = ETH_GENESIS]',
    )
    parser.add_argument(
        '--end-date',
        help='end date to use [default = now]',
    )
    parser.add_argument('--root-dir', help='root data directory')
    parser.add_argument('--datasets', help='datasets to use')
    parser.set_defaults(f_command=collect_command)
    if include_dashboard_arg:
        parser.add_argument('dashboard', help='dashboard to collect data of')
    cli_parsing.add_common_args(parser)


def collect_command(
    args: argparse.Namespace,
    dashboard: str | typing.Type[types.Dashboard] | None = None,
) -> None:
    registry: types.RegistryFile = {
        'path': args.registry,
        'validate': not args.no_validate,
    }
    if dashboard is None:
        dashboard = args.dashboard
    ops.collect_dashboard_data(dashboard=dashboard, registry=registry)
