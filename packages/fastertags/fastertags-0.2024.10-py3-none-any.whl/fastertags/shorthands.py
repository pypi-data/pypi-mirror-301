from collections.abc import Collection
from typing import Literal

from . import elements as el
from ._elements import HTMLElement, Content


def viewport(v: str, /) -> el.meta:
    return el.meta(name="viewport", content=v)


def charset(v: str, /) -> el.meta:
    return el.meta(charset=v)


type HTMXFlag = Literal[
    "allowEval",
    "allowNestedOobSwaps",
    "allowScriptTags",
    "defaultFocusScroll",
    "getCacheBusterParam",
    "globalViewTransitions",
    "historyEnabled",
    "ignoreTitle",
    "refreshOnHistoryMiss",
    "scrollIntoViewOnBoost",
    "selfRequestsOnly",
]


def htmxflag(flag: HTMXFlag, value: bool) -> el.script:
    return el.script(f"htmx.config.{flag} = {'true' if value else 'false'};")


def document(
    *,
    title: str,
    body: Content,
    lang: str = "en-US",
    direction: str = "ltr",
    script_sources: Collection[str] = ("https://unpkg.com/htmx.org@2.0.2",),
    viewport_width: str = "device-width",
    initial_scale: float = 1.0,
    viewport_fit: str = "cover",
) -> HTMLElement:
    return el.html(
        lang=lang,
        dir=direction,
    )(
        el.head(
            el.title(title),
            charset("utf8"),
            viewport(
                f"width={viewport_width}, initial-scale={initial_scale}, viewport-fit={viewport_fit}"
            ),
            *(el.script(src=src) for src in script_sources),
            htmxflag("selfRequestsOnly", False),
        ),
        el.body(body),
    )
