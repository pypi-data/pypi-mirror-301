from collections.abc import Collection
from typing import Literal

from ._elements import HTMLElement, Content
from .elements import meta, script, html, head, title as _title, body as _body


def viewport(v: str, /) -> meta:
    return meta(name="viewport", content=v)


def charset(v: str, /) -> meta:
    return meta(charset=v)


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


def htmxflag(flag: HTMXFlag, value: bool) -> script:
    return script(f"htmx.config.{flag} = {'true' if value else 'false'};")


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
    return html(
        lang=lang,
        dir=direction,
    )(
        head(
            _title(title),
            charset("utf8"),
            viewport(
                f"width={viewport_width}, initial-scale={initial_scale}, viewport-fit={viewport_fit}"
            ),
            *(script(src=src) for src in script_sources),
            htmxflag("selfRequestsOnly", False),
        ),
        _body(body),
    )
