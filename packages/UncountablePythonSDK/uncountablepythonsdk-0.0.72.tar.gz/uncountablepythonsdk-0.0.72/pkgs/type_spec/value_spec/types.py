from dataclasses import dataclass

from main.base.types import value_spec_t

from ..util import ParsedTypePath


@dataclass(kw_only=True, frozen=True)
class ParsedFunctionArgument:
    ref_name: str
    pass_null: bool
    extant: value_spec_t.ArgumentExtant
    type_path: ParsedTypePath


@dataclass(kw_only=True, frozen=True)
class ParsedFunctionSignature:
    arguments: list[ParsedFunctionArgument]
    return_type_path: ParsedTypePath
