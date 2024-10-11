from __future__ import annotations

from typing import Any, Literal, Union
from typing_extensions import TypedDict, NotRequired
from .dashboards.dashboard import Dashboard

import polars as pl
import tooltime


#
# # schema specification
#

Interval = Literal['point', 'day', 'week', 'month', 'year']

ColumnType = Union[pl.datatypes.classes.DataTypeClass, pl.datatypes.DataType]


class DataSchema(TypedDict):
    columns: dict[str, ColumnType]
    group_columns: list[str]


class DataSchemaPartial(TypedDict, total=False):
    columns: dict[str, ColumnType | None] | list[str]
    group_columns: list[str]


class MetricSpec(TypedDict):
    unit: str | None
    type: Literal[
        'point_in_time',
        'sum',
        'min',
        'max',
        'unique',
    ]


#
# # ui spec
#

StateDatum = Union[str, int, float]


class UiSpec(TypedDict):
    name: str
    title: str | None
    description: str | None
    version: str | None
    groupings: list[str]
    default_state: dict[str, StateDatum]
    invalid_states: list[dict[str, StateDatum]]
    inputs: dict[str, InputSpec]
    metrics: dict[str, MetricSpec]
    submetrics: dict[str, list[str]]
    shortcuts: dict[str, ShortcutSpec]
    colors: dict[str, str]
    schema: DataSchema


class InputSpec(TypedDict):
    type: Literal['button', 'date']
    description: str
    default: str
    visibility: NotRequired[InputVisibility]
    button_options: NotRequired[list[str]]
    date_options: NotRequired[list[str]]
    aliases: dict[str, StateDatum]


class InputVisibility(TypedDict):
    start_hidden: NotRequired[bool]
    hide_if: NotRequired[list[dict[str, Any]]]
    show_if: NotRequired[list[dict[str, Any]]]
    hide: NotRequired[bool]
    f: NotRequired[Any]  # function


class ShortcutSpec(TypedDict):
    action: Literal[
        'select',
        'cycle_next',
        'cycle_previous',
        'toggle_ui',
        'increment',
        'decrement',
    ]
    field: str | None
    value: NotRequired[str]
    help: NotRequired[str]


#
# # registry types
#


class Registry(TypedDict):
    mince_version: str
    dashboards: dict[str, 'RegistryEntry']


class RegistryFile(TypedDict):
    path: str | None
    validate: NotRequired[bool]
    create_if_dne: NotRequired[bool]


RegistryReference = Union[Registry, RegistryFile, str, None]


class RegistryEntry(TypedDict):
    dashboard: str
    name: str
    description: str | None
    data_dir: str | None
    use_disk_cache: bool


#
# # manager functions kwargs
#


class SpecKwargs(TypedDict):
    name: NotRequired[str | None]
    description: NotRequired[str | None]
    date_range: NotRequired[
        tuple[tooltime.Timestamp | None, tooltime.Timestamp | None]
    ]


class SpecKwargsPartial(TypedDict):
    name: NotRequired[str | None]
    description: NotRequired[str | None]
    date_range: NotRequired[
        tuple[tooltime.Timestamp | None, tooltime.Timestamp | None]
    ]


class LoadKwargs(TypedDict):
    data_dir: str | None
    datasets: list[str] | None


class LoadKwargsPartial(TypedDict):
    data_dir: NotRequired[str | None]
    datasets: NotRequired[list[str] | None]


class CollectKwargs(TypedDict):
    data_dir: str | None
    datasets: NotRequired[list[str] | None]


class CollectKwargsPartial(TypedDict):
    data_dir: NotRequired[str | None]
    datasets: NotRequired[list[str] | None]


#
# # validation
#


def validate_typeddict(typed_dict: Any, td_class: type) -> None:
    annotations = td_class.__annotations__

    for field_name, field_type in annotations.items():
        if field_name not in typed_dict:
            raise ValueError(f'Missing required field: {field_name}')

        value = typed_dict[field_name]

        if field_type == pl.DataType:
            if not isinstance(value, pl.DataType):
                raise TypeError(f'Field {field_name} must be a polars DataType')
        elif isinstance(field_type, type):
            if not isinstance(value, field_type):
                raise TypeError(
                    f'Field {field_name} must be of type {field_type}'
                )
        else:
            # Handle more complex types (e.g., Union, List, etc.) here
            # This might require more sophisticated type checking
            pass

    # Check for extra fields
    extra_fields = set(typed_dict.keys()) - set(annotations.keys())
    if extra_fields:
        raise ValueError(f"Unexpected extra fields: {', '.join(extra_fields)}")
