"""perform dashboard management actions"""

from __future__ import annotations

import typing

from mince import transforms
from ..dashboards.dashboard import Dashboard
from .. import ops
from . import disk_cache

if typing.TYPE_CHECKING:
    from typing import Type
    import tooltime
    import polars as pl
    from mince import types


def run_dashboard(
    dashboard: str | Type[Dashboard],
    *,
    ui_spec_kwargs: types.SpecKwargsPartial | None = None,
    data_kwargs: types.LoadKwargsPartial | None = None,
    run_kwargs: typing.Mapping[str, typing.Any] | None = None,
    registry: types.RegistryReference = None,
    cache: bool = True,
    cache_save: bool = True,
    cache_load: bool = True,
) -> None:
    instance = instantiate_dashboard(
        dashboard=dashboard,
        ui_spec_kwargs=ui_spec_kwargs,
        data_kwargs=data_kwargs,
        run_kwargs=run_kwargs,
        registry=registry,
        cache=cache,
        cache_save=cache_save,
        cache_load=cache_load,
    )

    # run dashboard
    if run_kwargs is None:
        run_kwargs = {}
    instance.run(**run_kwargs)


def instantiate_dashboard(
    dashboard: str | Type[Dashboard],
    *,
    ui_spec_kwargs: types.SpecKwargsPartial | None = None,
    data_kwargs: types.LoadKwargsPartial | None = None,
    run_kwargs: typing.Mapping[str, typing.Any] | None = None,
    registry: types.RegistryReference = None,
    cache: bool = True,
    cache_save: bool = True,
    cache_load: bool = True,
) -> Dashboard:
    # load data and spec
    dfs = load_dashboard_data(
        dashboard=dashboard,
        kwargs=data_kwargs,
        registry=registry,
        cache=cache,
        cache_save=cache_save,
        cache_load=cache_load,
    )

    date_ranges = [transforms.get_date_range(df) for df in dfs.values()]
    date_range = (
        min(min_date for (min_date, _) in date_ranges),
        max(max_date for (_, max_date) in date_ranges),
    )
    ui_spec = load_dashboard_ui_spec(
        dashboard=dashboard,
        kwargs=ui_spec_kwargs,
        registry=registry,
        date_range=date_range,
    )

    # create dashboard instance
    if isinstance(dashboard, str):
        DashboardClass = ops.get_dashboard_class(dashboard, registry=registry)
    elif issubclass(dashboard, Dashboard):
        DashboardClass = dashboard
    else:
        raise Exception()
    return DashboardClass(dfs=dfs, spec=ui_spec)


def load_dashboard_data(
    *,
    dashboard: str | type[Dashboard],
    kwargs: types.LoadKwargsPartial | None = None,
    registry: types.RegistryReference = None,
    cache: bool | None = None,
    cache_save: bool = True,
    cache_load: bool = True,
    data_dir: str | None = None,
) -> dict[str, pl.DataFrame]:
    import polars as pl

    if isinstance(dashboard, str):
        config = ops.get_dashboard_config(dashboard, registry=registry)
        if data_dir is None:
            data_dir = config['data_dir']
        if cache is None:
            cache = config['use_disk_cache']
        dashboard = ops.get_dashboard_class(dashboard, registry=registry)

    # load from cache
    if cache is None:
        cache = True
    last_collected = None
    if cache and cache_load:
        last_collected = dashboard.data_last_collected(data_dir=data_dir)
        if last_collected is not None:
            most_recent_cache = disk_cache.get_latest_cache_timestamp(dashboard)
            if (
                most_recent_cache is not None
                and most_recent_cache >= last_collected
            ):
                print('loading cache data for ' + dashboard.__name__)
                item = disk_cache.load_from_cache(
                    dashboard, timestamp=most_recent_cache
                )
                if item is not None:
                    return item

    # execute data
    if kwargs is None:
        kwargs = {}
    dfs = dashboard.load_data(**kwargs)

    # check type
    if (not isinstance(dfs, dict)) or any(
        not isinstance(name, str) or not isinstance(df, pl.DataFrame)
        for name, df in dfs.items()
    ):
        raise Exception('invalid format for data')

    # save to cache
    if cache and cache_save:
        if last_collected is None:
            last_collected = dashboard.data_last_collected(data_dir=data_dir)
        if last_collected is None:
            maxes = [
                df['timestamp'].max() for df in dfs.values() if len(df) > 0
            ]
            if len(maxes) > 0:
                import tooltime

                last_collected = tooltime.timestamp_to_seconds(max(maxes))  # type: ignore
        if last_collected is not None:
            print('saving data for ' + dashboard.__name__ + ' to cache')
            disk_cache.save_to_cache(
                dashboard=dashboard, dfs=dfs, timestamp=last_collected
            )

    return dfs


def load_dashboard_ui_spec(
    dashboard: str | type[Dashboard],
    kwargs: types.SpecKwargsPartial | None = None,
    registry: types.RegistryReference = None,
    validate: bool = False,
    *,
    date_range: tuple[tooltime.Timestamp, tooltime.Timestamp] | None = None,
) -> types.UiSpec:
    if isinstance(dashboard, str):
        dashboard = ops.get_dashboard_class(dashboard, registry=registry)

    if kwargs is None:
        kwargs = {}
    if date_range is not None:
        kwargs = dict(kwargs)  # type: ignore
        kwargs['date_range'] = date_range
    ui_spec = dashboard.load_spec(**kwargs)

    # validate spec
    if validate:
        from .. import types

        types.validate_typeddict(dict(ui_spec), types.UiSpec)

    return ui_spec


def collect_dashboard_data(
    dashboard: str | Type[Dashboard],
    *,
    kwargs: types.CollectKwargsPartial | None = None,
    registry: types.RegistryReference = None,
    data_dir: str | None = None,
) -> None:
    if isinstance(dashboard, str):
        config = ops.get_dashboard_config(dashboard, registry=registry)
        if data_dir is None:
            data_dir = config['data_dir']
        dashboard = ops.get_dashboard_class(dashboard, registry=registry)

    if kwargs is None:
        kwargs = {}
    if kwargs.get('data_dir') is None:
        kwargs['data_dir'] = data_dir

    dashboard.collect_data(**kwargs)
