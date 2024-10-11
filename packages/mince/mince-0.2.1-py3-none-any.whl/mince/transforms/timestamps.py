from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import polars as pl


def get_date_range(df: pl.DataFrame) -> tuple[int, int]:
    import datetime
    import tooltime

    if len(df) == 0:
        raise Exception('empty dataframe')

    start_time: datetime.datetime = df['timestamp'].min()  # type: ignore
    end_time: datetime.datetime = df['timestamp'].max()  # type: ignore

    return (
        tooltime.timestamp_to_seconds(start_time),
        tooltime.timestamp_to_seconds(end_time),
    )
