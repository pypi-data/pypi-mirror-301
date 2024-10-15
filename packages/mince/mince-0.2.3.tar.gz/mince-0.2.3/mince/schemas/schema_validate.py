from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from mince import types
    import polars as pl


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
