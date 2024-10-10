# DO NOT MODIFY -- This file is generated by type_spec
# flake8: noqa: F821
# ruff: noqa: E402 Q003
# fmt: off
# isort: skip_file
from __future__ import annotations
import typing  # noqa: F401
import datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
import dataclasses
from pkgs.serialization import serial_class
from pkgs.serialization import OpaqueKey
from ... import base_t
from ... import entity_t

__all__: list[str] = [
    "Arguments",
    "ColumnAccess",
    "Data",
    "ENDPOINT_METHOD",
    "ENDPOINT_PATH",
    "EntityResult",
]

ENDPOINT_METHOD = "GET"
ENDPOINT_PATH = "api/external/entity/external_list_entities"


# DO NOT MODIFY -- This file is generated by type_spec
@serial_class(
    unconverted_values={"attributes"},
)
@dataclasses.dataclass(kw_only=True)
class Arguments:
    config_reference: str
    entity_type: typing.Optional[entity_t.EntityType] = None
    attributes: typing.Optional[dict[OpaqueKey, base_t.JsonValue]] = None
    offset: typing.Optional[typing.Optional[int]] = None
    limit: typing.Optional[typing.Optional[int]] = None


# DO NOT MODIFY -- This file is generated by type_spec
@serial_class(
    unconverted_values={"column_values"},
)
@dataclasses.dataclass(kw_only=True)
class EntityResult:
    entity: entity_t.Entity
    column_values: list[base_t.JsonValue]


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class ColumnAccess:
    name: str
    table_label: typing.Optional[str]


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class Data:
    columns: list[ColumnAccess]
    results: list[EntityResult]
# DO NOT MODIFY -- This file is generated by type_spec
