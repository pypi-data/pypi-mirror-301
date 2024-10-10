import io
from dataclasses import dataclass, field

from . import builder, util
from .config import TypeScriptConfig

INDENT = "  "

MODIFY_NOTICE = "// DO NOT MODIFY -- This file is generated by type_spec\n"


@dataclass(kw_only=True)
class EmitTypescriptContext:
    config: TypeScriptConfig
    out: io.StringIO
    namespace: builder.SpecNamespace
    namespaces: set[builder.SpecNamespace] = field(default_factory=set)


def ts_type_name(name: str) -> str:
    return "".join([x.title() for x in name.split("_")])


def resolve_namespace_ref(namespace: builder.SpecNamespace) -> str:
    return f"{ts_type_name(namespace.name)}T"


def ts_name(name: str, name_case: builder.NameCase) -> str:
    if name_case == builder.NameCase.preserve:
        return name
    bits = util.split_any_name(name)
    return "".join([bits[0], *[x.title() for x in bits[1:]]])
