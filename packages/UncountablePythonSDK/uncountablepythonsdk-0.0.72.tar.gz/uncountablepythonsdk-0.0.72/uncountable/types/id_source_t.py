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
from . import entity_t

__all__: list[str] = [
    "IdSourceSpec",
    "IdSourceSpecBase",
    "IdSourceSpecCustomEntity",
    "IdSourceSpecEntity",
    "IdSourceSpecFieldOptions",
]


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class IdSourceSpecBase:
    pass


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class IdSourceSpecEntity(IdSourceSpecBase):
    entity_type: entity_t.EntityType


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class IdSourceSpecCustomEntity(IdSourceSpecBase):
    definition_ref_name: str


# DO NOT MODIFY -- This file is generated by type_spec
@dataclasses.dataclass(kw_only=True)
class IdSourceSpecFieldOptions(IdSourceSpecBase):
    set_ref_name: str
    subset_ref_name: typing.Optional[str] = None


# DO NOT MODIFY -- This file is generated by type_spec
IdSourceSpec = typing.Union[IdSourceSpecEntity, IdSourceSpecCustomEntity, IdSourceSpecFieldOptions]
# DO NOT MODIFY -- This file is generated by type_spec
