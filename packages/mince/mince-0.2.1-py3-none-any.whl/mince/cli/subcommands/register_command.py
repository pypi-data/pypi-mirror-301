from __future__ import annotations

import argparse
import typing

from ... import ops
from .. import cli_helpers

if typing.TYPE_CHECKING:
    from mince import types


def add_register_command(
    subparsers: cli_helpers.Subparsers, include_dashboard_arg: bool
) -> None:
    parser = subparsers.add_parser(
        'register',
        help='register dashboard',
        formatter_class=cli_helpers.HelpFormatter,
    )
    parser.set_defaults(f_command=register_command)
    parser.add_argument(
        'dashboard_class',
        metavar='MODULE:CLASS',
        help='Dashboard class',
    )
    parser.add_argument(
        '--name',
        help='name of dashboard',
    )
    parser.add_argument(
        '--description',
        help='description of dashboard',
    )
    cli_helpers.add_common_args(parser)


def register_command(
    args: argparse.Namespace,
    dashboard: str | typing.Type[types.Dashboard] | None = None,
) -> None:
    registry: types.RegistryFile = {
        'path': args.registry,
        'validate': not args.no_validate,
    }
    if dashboard is None:
        dashboard = args.dashboard_class
    ops.register_dashboard(
        dashboard=dashboard,
        name=args.name,
        description=args.description,
        registry=registry,
    )
