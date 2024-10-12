import builtins
import json
import keyword
import re
from itertools import chain
from pathlib import Path
from typing import Final

_RESERVED: Final[set[str]] = {
    "args",
    "kwargs",
    "self",
}

_TR: Final = str.maketrans({"-": "_"})

_ADDITIONAL_ARGS: Final[
    dict[str, dict[str, tuple[type[bool], bool | None] | tuple[type[str], str | None]]]
] = {
    "style": {
        "scoped": (bool, None),
    },
}

_ELEM_ORDER: Final[tuple[str, ...]] = (
    "head",
    "body",
    "html",
)


def _san(n: str) -> str:
    n = n.translate(_TR)
    if keyword.iskeyword(n) or n in _RESERVED:
        return f"{n}_"
    return n


_CONTENT_TYPE: Final[dict[str, str]] = {
    "*": "Content",
    "style": "str",
    "script": "str",
    "textarea": "str",
    "html": "SpecificContent[head | body]",
}

_ATTRIBUTE_TYPES: Final[dict[str, dict[str, str]]] = {
    "*": {
        "class": "str | Collection[str]",
    },
}


def _atttype(elem, attr, type_) -> str:
    if elem in _ATTRIBUTE_TYPES and attr in _ATTRIBUTE_TYPES[elem]:
        return _ATTRIBUTE_TYPES[elem][attr]
    if "*" in _ATTRIBUTE_TYPES and attr in _ATTRIBUTE_TYPES["*"]:
        return _ATTRIBUTE_TYPES["*"][attr]
    return type_


if __name__ == "__main__":
    parent = Path(__file__).parent

    with open(parent / "elements.json", encoding="utf8") as f:
        elems = json.load(f)
        elems["*"]["attributes"] = {
            k: v for k, v in elems["*"]["attributes"].items() if not k.startswith("on")
        }

    order = ["*", *_ELEM_ORDER, *(e for e in elems.keys() if e not in _ELEM_ORDER)]
    elems = {k: elems[k] for k in sorted(elems.keys(), key=order.index)}

    builtin_names: frozenset[str] = frozenset(dir(builtins))

    def _pylint_el(elem):
        elem = _san(elem)
        if elem in builtin_names:
            return "  # pylint: disable=redefined-builtin"
        return ""

    def _pylint(attr):
        attr = _san(attr)
        if attr in builtin_names:
            return "  # pylint: disable=redefined-builtin"
        if attr in elems:
            return "  # pylint: disable=redefined-outer-name"
        return ""

    with open(parent / "elements.py", "w", encoding="utf8") as fe:

        def write(*args):
            # noinspection PyTypeChecker
            print(*args, sep="\n", file=fe)

        write(
            "from collections.abc import Collection",
            "from ._elements import Content, SpecificContent, HTMLElement",
        )
        for el, em in elems.items():
            is_empty = em["empty"]
            attrs = em["attributes"]
            if el == "*":
                continue
            content_type = _CONTENT_TYPE.get(el) or _CONTENT_TYPE["*"]
            write(
                "# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames",
                f"class {_san(el)}(HTMLElement):{_pylint_el(el)}",
                f"  EMPTY = {is_empty}",
                f'  TAG = "{el}"',
                r"  def __init__(",
                r"    self,",
                *(
                    []
                    if is_empty
                    else [
                        f"    *args: {content_type},",
                    ]
                ),
                *chain.from_iterable(
                    [
                        f"    {_san(attr)}: {_atttype(el, attr, type_)} | None = None,{_pylint(attr)}",
                    ]
                    for attr, type_ in attrs.items()
                ),
                *chain.from_iterable(
                    [
                        f"    {_san(attr)}: {_atttype(el, attr, type_)} | None = None,{_pylint(attr)}",
                    ]
                    for attr, type_ in elems["*"]["attributes"].items()
                    if attr not in attrs
                ),
                *chain.from_iterable(
                    [
                        f"    {_san(attr)}: {type_.__name__} | None = {repr(default_value or None)},{_pylint(attr)}",
                    ]
                    for attr, (type_, default_value) in _ADDITIONAL_ARGS.get(
                        el, {}
                    ).items()
                ),
                "    **kwargs: str | bool | Collection[str] | None,",
                "  ):",
                "    super().__init__()",
                "    for k, v in kwargs.items():",
                "      self[k] = v",
                *chain.from_iterable(
                    [
                        f"    if {_san(attr)} is not None:",
                        f"      self['{attr}'] = {_san(attr)}",
                    ]
                    for attr, type_ in attrs.items()
                ),
                *chain.from_iterable(
                    [
                        f"    if {_san(attr)} is not None:",
                        f"      self['{attr}'] = {_san(attr)}",
                    ]
                    for attr, type_ in elems["*"]["attributes"].items()
                    if attr not in attrs
                ),
                *chain.from_iterable(
                    [
                        f"    if {_san(attr)} is not None:",
                        f"      self['{attr}'] = {_san(attr)}",
                    ]
                    for attr, _ in _ADDITIONAL_ARGS.get(el, {}).items()
                ),
                *(
                    []
                    if is_empty
                    else [
                        r"    self(*args)",
                        f"  def __call__(self, *args: {content_type}) -> HTMLElement:",
                        r"    self._content.extend(args)",
                        r"    return self",
                    ]
                ),
            )

    with open(parent / "__init__.py", "r", encoding="utf8") as fp:
        init_file = fp.read()

    init_file = re.sub(
        r"# codegen: begin\[imports]\n.+# codegen: end\[imports]\n",
        "".join(
            [
                "# codegen: begin[imports]\n",
                "from .elements import (  # pylint: disable=redefined-builtin\n",
                *(f"  {_san(el)},\n" for el in sorted(elems.keys()) if el != "*"),
                ")\n",
                "# codegen: end[imports]\n",
            ]
        ),
        init_file,
        flags=re.DOTALL,
    )
    init_file = re.sub(
        r"# codegen: begin\[__all__]\n.+# codegen: end\[__all__]\n",
        "".join(
            [
                "# codegen: begin[__all__]\n",
                *(f"  '{_san(el)}',\n" for el in sorted(elems.keys()) if el != "*"),
                "# codegen: end[__all__]\n",
            ]
        ),
        init_file,
        flags=re.DOTALL,
    )

    with open(parent / "__init__.py", "w", encoding="utf8") as fp:
        fp.write(init_file)
