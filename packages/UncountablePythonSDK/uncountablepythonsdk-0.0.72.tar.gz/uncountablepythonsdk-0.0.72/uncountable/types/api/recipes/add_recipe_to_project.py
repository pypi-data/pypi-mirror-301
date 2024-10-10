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
from ... import identifier_t

__all__: list[str] = [
    "Arguments",
    "Data",
    "ENDPOINT_METHOD",
    "ENDPOINT_PATH",
]

ENDPOINT_METHOD = "POST"
ENDPOINT_PATH = "api/external/recipes/add_recipe_to_project"


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class Arguments:
    recipe_key: identifier_t.IdentifierKey
    project_key: identifier_t.IdentifierKey


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class Data:
    pass
# DO NOT MODIFY -- This file is generated by type_spec
