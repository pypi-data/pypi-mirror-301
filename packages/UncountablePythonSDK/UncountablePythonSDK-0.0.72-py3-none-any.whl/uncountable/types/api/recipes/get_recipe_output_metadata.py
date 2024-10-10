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
from ... import base_t
from ... import recipe_output_metadata_t

__all__: list[str] = [
    "Arguments",
    "Data",
    "ENDPOINT_METHOD",
    "ENDPOINT_PATH",
    "RecipeOutputMetadata",
]

ENDPOINT_METHOD = "GET"
ENDPOINT_PATH = "api/external/recipes/external_get_recipe_output_metadata"


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class Arguments:
    recipe_output_ids: list[base_t.ObjectId]


# DO NOT MODIFY -- This file is generated by type_spec
@serial_class(
    unconverted_values={"quantity_json"},
    to_string_values={"quantity_dec"},
)
@dataclasses.dataclass(kw_only=True)
class RecipeOutputMetadata:
    recipe_output_id: base_t.ObjectId
    recipe_output_metadata_field_id: base_t.ObjectId
    quantity_dec: Decimal
    quantity_json: base_t.JsonValue


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class Data:
    recipe_output_metadata: list[RecipeOutputMetadata]
    recipe_output_metadata_fields: list[recipe_output_metadata_t.RecipeOutputMetadataField]
# DO NOT MODIFY -- This file is generated by type_spec
