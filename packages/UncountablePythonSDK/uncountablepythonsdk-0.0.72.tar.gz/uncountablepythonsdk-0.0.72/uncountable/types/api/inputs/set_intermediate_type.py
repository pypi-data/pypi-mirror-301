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
from ... import identifier_t

__all__: list[str] = [
    "Arguments",
    "Data",
    "ENDPOINT_METHOD",
    "ENDPOINT_PATH",
    "IntermediateType",
]

ENDPOINT_METHOD = "POST"
ENDPOINT_PATH = "api/external/inputs/set_intermediate_type"


# DO NOT MODIFY -- This file is generated by type_spec
class IntermediateType(StrEnum):
    FINAL_PRODUCT = "final_product"
    COMPOUND_AS_INTERMEDIATE = "compound_as_intermediate"


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class Arguments:
    input_key: identifier_t.IdentifierKey
    intermediate_type: IntermediateType


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class Data:
    pass
# DO NOT MODIFY -- This file is generated by type_spec
