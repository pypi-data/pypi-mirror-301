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
from ... import async_batch_t
from ... import entity_t
from ... import identifier_t

__all__: list[str] = [
    "Arguments",
    "Data",
    "ENDPOINT_METHOD",
    "ENDPOINT_PATH",
]

ENDPOINT_METHOD = "POST"
ENDPOINT_PATH = "api/external/entity/external_lock_entity"


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class Arguments:
    entity_key: identifier_t.IdentifierKey
    entity_type: entity_t.EntityType
    globally_removable: typing.Optional[bool] = None


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class Data(async_batch_t.AsyncBatchActionReturn):
    pass
# DO NOT MODIFY -- This file is generated by type_spec
