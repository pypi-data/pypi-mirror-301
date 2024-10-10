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
from ... import base_t
from ... import id_source_t

__all__: list[str] = [
    "Arguments",
    "Data",
    "ENDPOINT_METHOD",
    "ENDPOINT_PATH",
    "Match",
]

ENDPOINT_METHOD = "GET"
ENDPOINT_PATH = "api/external/id_source/match_id_source"


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class Arguments:
    spec: id_source_t.IdSourceSpec
    names: list[str]


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class Match:
    name: str
    ids: list[typing.Union[base_t.ObjectId, str]]


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class Data:
    results: list[Match]
# DO NOT MODIFY -- This file is generated by type_spec
