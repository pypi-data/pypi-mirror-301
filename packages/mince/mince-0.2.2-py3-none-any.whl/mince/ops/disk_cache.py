from __future__ import annotations

import os
import typing

if typing.TYPE_CHECKING:
    from typing import Type
    import polars as pl
    import tooltime

    from ..dashboards.dashboard import Dashboard


def save_to_cache(
    dashboard: type[Dashboard],
    dfs: dict[str, pl.DataFrame],
    timestamp: tooltime.Timestamp,
) -> None:
    cache_dir = get_cache_dir(dashboard=dashboard, timestamp=timestamp)
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
    for key, df in dfs.items():
        path = get_cache_filepath(dashboard, timestamp, key)
        print(path)
        df.write_parquet(path)


def load_from_cache(
    dashboard: type[Dashboard],
    *,
    timestamp: tooltime.Timestamp | None = None,
) -> dict[str, pl.DataFrame] | None:
    import polars as pl

    if timestamp is None:
        timestamp = get_latest_cache_timestamp(dashboard)
        if timestamp is None:
            return None
    cache_dir = get_cache_dir(dashboard=dashboard, timestamp=timestamp)
    data = {}
    if not os.path.isdir(cache_dir):
        return None
    for filename in os.listdir(cache_dir):
        name = filename.split('.parquet')[0]
        data[name] = pl.read_parquet(os.path.join(cache_dir, filename))
    return data


def get_latest_cache_timestamp(dashboard: type[Dashboard]) -> int | None:
    root = '/tmp/mince/data_cache'
    prefix = get_cache_name(dashboard) + '__'
    if not os.path.isdir(root):
        return None
    cache_dirs = [path for path in os.listdir(root) if path.startswith(prefix)]
    if len(cache_dirs) > 0:
        return int(sorted(cache_dirs)[0].split('__')[-1])
    else:
        return None


def get_cache_dir(
    dashboard: type[Dashboard], timestamp: tooltime.Timestamp
) -> str:
    import tooltime

    timestamp = tooltime.timestamp_to_seconds(timestamp)
    template = '/tmp/mince/data_cache/{dashboard}__{timestamp}'
    name = get_cache_name(dashboard)
    return template.format(dashboard=name, timestamp=timestamp)


def get_cache_filepath(
    dashboard: type[Dashboard], timestamp: tooltime.Timestamp, data: str
) -> str:
    cache_dir = get_cache_dir(dashboard=dashboard, timestamp=timestamp)
    template = os.path.join(cache_dir, '{data}.parquet')
    return template.format(data=data)


def get_cache_name(dashboard: Type[Dashboard]) -> str:
    # get version
    import importlib

    module = importlib.import_module(dashboard.__module__)
    if module.__package__ is not None:
        package = importlib.import_module(module.__package__)
        container = package
    else:
        container = module
    try:
        version = container.__version__
    except AttributeError:
        version = 'no_version'

    return (
        str(dashboard.__module__)
        + '.'
        + str(dashboard.__name__)
        + '_'
        + str(version)
    )
