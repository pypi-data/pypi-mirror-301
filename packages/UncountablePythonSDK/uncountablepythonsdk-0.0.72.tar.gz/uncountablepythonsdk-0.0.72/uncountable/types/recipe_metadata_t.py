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
from . import base_t

__all__: list[str] = [
    "MetadataValue",
    "RecipeMetadata",
    "SimpleRecipeMetadataField",
]


# DO NOT MODIFY -- This file is generated by type_spec
@serial_class(
    unconverted_values={"value_json"},
    to_string_values={"value_numeric"},
)
@dataclasses.dataclass(kw_only=True)
class MetadataValue:
    metadata_id: base_t.ObjectId
    value_numeric: typing.Optional[Decimal] = None
    value_str: typing.Optional[str] = None
    value_json: typing.Optional[base_t.JsonValue] = None
    value_file_ids: typing.Optional[list[base_t.ObjectId]] = None


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class SimpleRecipeMetadataField:
    metadata_id: base_t.ObjectId
    name: str
    quantity_type: str


# DO NOT MODIFY -- This file is generated by type_spec
@serial_class(
    unconverted_values={"quantity_json"},
    to_string_values={"quantity_dec"},
)
@dataclasses.dataclass(kw_only=True)
class RecipeMetadata:
    metadata_id: base_t.ObjectId
    quantity_dec: typing.Optional[Decimal] = None
    quantity_json: typing.Optional[base_t.JsonValue] = None
# DO NOT MODIFY -- This file is generated by type_spec
