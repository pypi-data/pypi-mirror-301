"""utilities related to processing data schemas"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from mince import types
    import polars as pl


def get_series_columns(schema: dict[str, types.ColumnType]) -> list[str]:
    return [
        column
        for column in schema.keys()
        if column not in ['timestamp', 'value']
    ]


def get_default_columns() -> dict[str, types.ColumnType]:
    import polars as pl

    return {
        'metric': pl.String,
        'timestamp': pl.Datetime(time_unit='ms'),
        'interval': pl.String,  # point, day, week, month
        'value': pl.Float64,
    }


def partial_schema_to_whole(
    partial: types.DataSchemaPartial,
) -> types.DataSchema:
    import polars as pl

    raw_group_columns = partial.get('group_columns')
    if raw_group_columns is None:
        group_columns = []
    else:
        group_columns = raw_group_columns

    columns = {}
    raw_columns = partial.get('columns')
    if raw_columns is None:
        raise Exception('must specify columns')
    elif isinstance(raw_columns, list):
        default_columns = get_default_columns()
        for column in raw_columns:
            dtype = default_columns.get(column)
            if dtype is not None:
                columns[column] = dtype
            else:
                columns[column] = pl.String
    elif isinstance(raw_columns, dict):
        default_columns = get_default_columns()
        for column, dtype in raw_columns.items():
            if dtype is not None:
                columns[column] = dtype
            elif column in default_columns:
                columns[column] = default_columns[column]
            else:
                columns[column] = pl.String
    else:
        raise Exception('invalid column format')

    return {
        'columns': columns,
        'group_columns': group_columns,
    }


def get_blank_dataframe(ui_spec: types.UiSpec) -> pl.DataFrame:
    """get black dataframe conforming to data schema"""
    import polars as pl

    return pl.DataFrame([], schema=ui_spec['schema']['columns'])


def validate_schema(
    df: pl.DataFrame, schema: dict[str, types.ColumnType]
) -> None:
    """validate that df conforms to data schema"""
    import polars as pl

    if df.schema != schema:
        if set(df.columns) != set(schema.keys()):
            wrong_columns = (set(df.columns) - set(schema.keys())) | (
                set(schema.keys()) - set(df.columns)
            )
            raise Exception('wrong columns in schema: ' + str(wrong_columns))
        else:
            raise Exception('invalid schema')

    valid_intervals = {'point', 'day', 'week', 'month', 'year'}
    invalid_intervals = df[['interval']].filter(
        ~pl.col.interval.is_in(valid_intervals)
    )
    if len(invalid_intervals) > 0:
        raise Exception('invalid value for interval: ' + str(invalid_intervals))


def validate_data_matches_spec(
    dfs: dict[str, pl.DataFrame], spec: types.UiSpec
) -> None:
    for df in dfs.values():
        validate_schemas_equal(dict(df.schema), spec['schema']['columns'])


def validate_schemas_equal(
    data_schema: dict[str, Any], spec_schema: dict[str, Any]
) -> None:
    if data_schema == spec_schema:
        return None

    missing_columns = []
    for column in spec_schema:
        if column not in data_schema:
            missing_columns.append(column)
    if len(missing_columns) > 0:
        raise Exception(
            'data does not match schema, missing columns: '
            + str(missing_columns)
        )

    extra_columns = []
    for column in data_schema:
        if column not in spec_schema:
            extra_columns.append(column)
    if len(extra_columns) > 0:
        raise Exception(
            'data does not match schema, extra columns: ' + str(extra_columns)
        )

    different_types = {}
    for column in data_schema.keys():
        if data_schema[column] != spec_schema[column]:
            different_types[column] = (data_schema[column], spec_schema[column])
    if len(different_types) > 0:
        raise Exception(
            'data does not match schema, types do not match: '
            + str(different_types)
        )

    if list(data_schema.keys()) != list(spec_schema.keys()):
        raise Exception(
            'data does not match schema, columns are in wrong order'
        )

    raise Exception('data does not match schema, unknown difference')
