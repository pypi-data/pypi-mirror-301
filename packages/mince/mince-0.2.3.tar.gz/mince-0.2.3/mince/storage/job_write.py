from __future__ import annotations

import os
import typing

from . import paths
from . import job_read

if typing.TYPE_CHECKING:
    import polars as pl
    from mince import types


def write_job_results(
    job: types.CollectionJobSummary,
    dfs: dict[str, pl.DataFrame],
    mark_as_latest: bool | None = None,
) -> None:
    import json

    data_dir = job['collect_kwargs']['data_dir']

    # write metadata
    metadata_path = paths.get_job_metadata_path(
        dashboard=job['dashboard_name'],
        timestamp=job['job_start_time'],
        data_dir=data_dir,
    )
    os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
    with open(metadata_path, 'w') as f:
        json.dump(job, f)

    # write dataframes
    for datum_name, df in dfs.items():
        path = paths.get_job_datum_path(
            datum_name=datum_name,
            data_dir=data_dir,
            timestamp=job['job_start_time'],
        )
        df.write_parquet(path)

    # write latest.json file
    if mark_as_latest is None:
        latest_job = job_read.read_latest_job_summary(
            dashboard=job['dashboard_name']
        )
        if latest_job is None:
            mark_as_latest = True
        else:
            mark_as_latest = (
                job['job_start_time'] >= latest_job['job_start_time']
            )
    if mark_as_latest:
        latest_path = paths.get_job_latest_path(
            dashboard=job['dashboard_name'],
            data_dir=data_dir,
        )
        with open(latest_path, 'w') as f:
            json.dump(job, f)
