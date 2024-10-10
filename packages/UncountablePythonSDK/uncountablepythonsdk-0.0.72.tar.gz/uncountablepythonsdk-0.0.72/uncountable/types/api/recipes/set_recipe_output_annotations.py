# DO NOT MODIFY -- This file is generated by type_spec
# flake8: noqa: F821
# ruff: noqa: E402 Q003
# fmt: off
# isort: skip_file
from __future__ import annotations
import typing  # noqa: F401
import datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
from pkgs.strenum_compat import StrEnum
import dataclasses
from pkgs.serialization import serial_class
from pkgs.serialization import serial_union_annotation
from ... import base_t
from ... import identifier_t

__all__: list[str] = [
    "AnnotationEdit",
    "AnnotationUpdateType",
    "Arguments",
    "Data",
    "ENDPOINT_METHOD",
    "ENDPOINT_PATH",
    "RecipeOutputEditBase",
    "RecipeOutputMergeAnnotations",
    "RecipeOutputReplaceAnnotations",
    "RecipeOutputUpdateAnnotations",
]

ENDPOINT_METHOD = "POST"
ENDPOINT_PATH = "api/external/recipes/set_recipe_output_annotations"


# DO NOT MODIFY -- This file is generated by type_spec
@serial_class(
    to_string_values={"lower_value", "upper_value"},
)
@dataclasses.dataclass(kw_only=True)
class AnnotationEdit:
    annotation_type_key: identifier_t.IdentifierKey
    lower_value: typing.Optional[Decimal] = None
    upper_value: typing.Optional[Decimal] = None


# DO NOT MODIFY -- This file is generated by type_spec
class AnnotationUpdateType(StrEnum):
    MERGE = "merge"
    REPLACE = "replace"


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class RecipeOutputEditBase:
    recipe_id: base_t.ObjectId
    output_id: base_t.ObjectId
    experiment_num: int
    annotations: list[AnnotationEdit]
    condition_id: typing.Optional[base_t.ObjectId] = None


# DO NOT MODIFY -- This file is generated by type_spec
@serial_class(
    parse_require={"type"},
)
@dataclasses.dataclass(kw_only=True)
class RecipeOutputMergeAnnotations(RecipeOutputEditBase):
    type: typing.Literal[AnnotationUpdateType.MERGE] = AnnotationUpdateType.MERGE


# DO NOT MODIFY -- This file is generated by type_spec
@serial_class(
    parse_require={"type"},
)
@dataclasses.dataclass(kw_only=True)
class RecipeOutputReplaceAnnotations(RecipeOutputEditBase):
    type: typing.Literal[AnnotationUpdateType.REPLACE] = AnnotationUpdateType.REPLACE


# DO NOT MODIFY -- This file is generated by type_spec
RecipeOutputUpdateAnnotations = typing.Annotated[
    typing.Union[RecipeOutputMergeAnnotations, RecipeOutputReplaceAnnotations],
    serial_union_annotation(
        discriminator="type",
        discriminator_map={
            "merge": RecipeOutputMergeAnnotations,
            "replace": RecipeOutputReplaceAnnotations,
        },
    ),
]


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class Arguments:
    updates: list[RecipeOutputUpdateAnnotations]


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class Data:
    pass
# DO NOT MODIFY -- This file is generated by type_spec
