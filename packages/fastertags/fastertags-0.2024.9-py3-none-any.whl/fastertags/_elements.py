import re
import sys
from collections.abc import Callable, Collection
from http import HTTPStatus
from io import StringIO
from typing import Any, Literal, Final, Self, IO, Iterable
from urllib.parse import quote

from .headers import Header

_REGULAR_NAME: Final[re.Pattern] = re.compile(r"^[A-Za-z0-9]+([_-][A-Za-z0-9]+)*$")
_SEPARATOR: Final[re.Pattern] = re.compile(r"[_-]")
_BOUNDARY: Final[re.Pattern] = re.compile(r"([A-Z]+|[a-z0-9]+)([A-Z]|$)")

_TR: Final = str.maketrans({"_": "-"})

type Event = Literal[
    "auxclick",
    "beforeinput",
    "beforematch",
    "beforetoggle",
    "blur",
    "cancel",
    "canplay",
    "canplaythrough",
    "change",
    "click",
    "close",
    "contextlost",
    "contextmenu",
    "contextrestored",
    "copy",
    "cuechange",
    "cut",
    "dblclick",
    "drag",
    "dragend",
    "dragenter",
    "dragleave",
    "dragover",
    "dragstart",
    "drop",
    "durationchange",
    "emptied",
    "ended",
    "error",
    "focus",
    "formdata",
    "input",
    "invalid",
    "keydown",
    "keypress",
    "keyup",
    "load",
    "loadeddata",
    "loadedmetadata",
    "loadstart",
    "mousedown",
    "mouseenter",
    "mouseleave",
    "mousemove",
    "mouseout",
    "mouseover",
    "mouseup",
    "paste",
    "pause",
    "play",
    "playing",
    "progress",
    "ratechange",
    "reset",
    "resize",
    "scroll",
    "scrollend",
    "securitypolicyviolation",
    "seeked",
    "seeking",
    "select",
    "slotchange",
    "stalled",
    "submit",
    "suspend",
    "timeupdate",
    "toggle",
    "volumechange",
    "waiting",
    "wheel",
    "htmx:abort",
    "htmx:afterOnLoad",
    "htmx:afterProcessNode",
    "htmx:afterRequest",
    "htmx:afterSettle",
    "htmx:afterSwap",
    "htmx:beforeCleanupElement",
    "htmx:beforeOnLoad",
    "htmx:beforeProcessNode",
    "htmx:beforeRequest",
    "htmx:beforeSwap",
    "htmx:beforeSend",
    "htmx:configRequest",
    "htmx:confirm",
    "htmx:historyCacheError",
    "htmx:historyCacheMiss",
    "htmx:historyCacheMissError",
    "htmx:historyCacheMissLoad",
    "htmx:historyRestore",
    "htmx:beforeHistorySave",
    "htmx:load",
    "htmx:noSSESourceError",
    "htmx:onLoadError",
    "htmx:oobAfterSwap",
    "htmx:oobBeforeSwap",
    "htmx:oobErrorNoTarget",
    "htmx:prompt",
    "htmx:pushedIntoHistory",
    "htmx:responseError",
    "htmx:sendError",
    "htmx:sseError",
    "htmx:sseOpen",
    "htmx:swapError",
    "htmx:targetError",
    "htmx:timeout",
    "htmx:validation:validate",
    "htmx:validation:failed",
    "htmx:validation:halted",
    "htmx:xhr:abort",
    "htmx:xhr:loadend",
    "htmx:xhr:loadstart",
    "htmx:xhr:progress",
]


def _normalize(attname: str) -> str:
    return attname.translate(_TR).strip("_-")


def htmlspecialchars(v: str) -> str:
    return v.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot")


def write(
    f: IO[str],
    objs: Iterable,
    *,
    oob_handler: Callable[[Any], None] | None,
    escape_html: bool = True,
    path: tuple[str, ...] = (),
) -> None:
    for obj in objs:
        if isinstance(obj, str):
            f.write(htmlspecialchars(obj) if escape_html else obj)
        elif isinstance(obj, HTMLElement):
            obj.print(f, oob_handler=oob_handler, end="", path=path)
        elif isinstance(obj, Iterable):
            write(f, obj, oob_handler=oob_handler, escape_html=escape_html)
        elif callable(oob_handler):
            oob_handler(obj)


type Content = HTMLElement | str | Iterable[Content] | Header | HTTPStatus
type SpecificContent[T] = T | Iterable[SpecificContent[T]] | Header | HTTPStatus
type Renderable = HTMLElement | str | Iterable[Renderable]


class HTMLElement:
    EVENT_HANDLER_PREFIX = "hx-on:"
    MINIMIZE_CSS = True

    EMPTY = False
    TAG = "*"

    def __init__(self) -> None:
        self._attvals: dict[str, Any] = dict()
        self._content: list[Content] = list()
        self._onevent: dict[str, list[str]] = dict()

    def __setitem__(self, name: str, value: Any):
        if isinstance(value, Collection) and not isinstance(value, str):
            value = " ".join(map(str, value))
        self._attvals[_normalize(name)] = value

    def __getitem__(self, name: str) -> str | bool | None:
        return self._attvals.get(_normalize(name))

    def __str__(self) -> str:
        ios = StringIO()
        self.print(ios, end="")
        return ios.getvalue()

    def print(
        self,
        file: IO[str] = sys.stdout,
        *,
        oob_handler: Callable[[Any], None] | None = None,
        end: str = "\n",
        path: tuple[str, ...] = (),
    ) -> None:
        if self.TAG == "html":
            file.write("<!DOCTYPE html>")
        file.write("<")
        file.write(self.TAG)
        for att, val in self._attvals.items():
            if self.TAG == "style" and att == "scoped":
                continue
            if isinstance(val, bool):
                if val:
                    file.write(" ")
                    file.write(att)
            else:
                file.write(" ")
                file.write(att)
                file.write('="')
                file.write(htmlspecialchars(val))
                file.write('"')
        for ev, vals in self._onevent.items():
            if len(vals) == 1:
                file.write(" ")
                file.write(self.EVENT_HANDLER_PREFIX)
                file.write(ev)
                file.write('="')
                file.write(htmlspecialchars(vals[0]))
                file.write('"')
        file.write(">")
        if self.EMPTY:
            return
        if self.TAG == "style":
            # write the contents of a style tag.  We emulate the "scoped" attribute by wrapping
            # the contents of the style into a `@scope { ... }` (unless scoped is False).
            is_scoped = self._attvals.get("scoped", None)
            if is_scoped is None:
                is_scoped = "head" not in path
            if is_scoped:
                file.write("@scope {")
            if self.MINIMIZE_CSS:
                # simple minification of CSS
                fs = StringIO()
                write(fs, self._content, oob_handler=oob_handler, escape_html=False)
                for ln in fs.getvalue().splitlines():
                    file.write(ln.strip())
            else:
                write(file, self._content, oob_handler=oob_handler, escape_html=False)
            if is_scoped:
                file.write("}")
        else:
            # write out the contents.  If the tag is <script>, do not escape special characters.
            write(
                file,
                self._content,
                oob_handler=oob_handler,
                escape_html=self.TAG != "script",
                path=path + (self.TAG,),
            )
        file.write("</")
        file.write(self.TAG)
        file.write(">")
        if end:
            file.write(end)

    def on(self, event: Event, handler: str) -> Self:
        if event not in self._onevent:
            self._onevent[event] = []
        self._onevent[event].append(handler)
        return self

    def hx(
        self,
        render: Renderable | None = None,
        get: str | None = None,
        post: str | None = None,
        push_url: str | None = None,
        select: str | None = None,
        select_oob: str | None = None,
        swap: str | None = None,
        swap_oob: str | None = None,
        target: str | None = None,
        trigger: str | None = None,
        vals: str | None = None,
        boost: str | None = None,
        confirm: str | None = None,
        delete: str | None = None,
        disable: str | None = None,
        disable_elt: str | None = None,
        disinherit: str | None = None,
        encoding: str | None = None,
        ext: str | None = None,
        headers: str | None = None,
        history: str | None = None,
        history_elt: str | None = None,
        include: str | None = None,
        indicator: str | None = None,
        inherit: str | None = None,
        params: str | None = None,
        patch: str | None = None,
        preserve: str | None = None,
        prompt: str | None = None,
        put: str | None = None,
        replace_url: str | None = None,
        request: str | None = None,
        sync: str | None = None,
        validate: str | None = None,
    ) -> Self:
        if render is not None:
            _fio = StringIO()
            write(_fio, [render], oob_handler=None)
            self["hx-get"] = f"data:text/html,{quote(_fio.getvalue())}"
        if get is not None:
            self["hx-get"] = get
        if post is not None:
            self["hx-post"] = post
        if push_url is not None:
            self["hx-push-url"] = push_url
        if select is not None:
            self["hx-select"] = select
        if select_oob is not None:
            self["hx-select-oob"] = select_oob
        if swap is not None:
            self["hx-swap"] = swap
        if swap_oob is not None:
            self["hx-swap-oob"] = swap_oob
        if target is not None:
            self["hx-target"] = target
        if trigger is not None:
            self["hx-trigger"] = trigger
        if vals is not None:
            self["hx-vals"] = vals
        if boost is not None:
            self["hx-boost"] = vals
        if confirm is not None:
            self["hx-confirm"] = confirm
        if delete is not None:
            self["hx-delete"] = delete
        if disable is not None:
            self["hx-disable"] = disable
        if disable_elt is not None:
            self["hx-disable-elt"] = disable_elt
        if disinherit is not None:
            self["hx-disinherit"] = disinherit
        if encoding is not None:
            self["hx-encoding"] = encoding
        if ext is not None:
            self["hx-ext"] = ext
        if headers is not None:
            self["hx-headers"] = headers
        if history is not None:
            self["hx-history"] = history
        if history_elt is not None:
            self["hx-history-elt"] = history_elt
        if include is not None:
            self["hx-include"] = include
        if indicator is not None:
            self["hx-indicator"] = indicator
        if inherit is not None:
            self["hx-inherit"] = inherit
        if params is not None:
            self["hx-params"] = params
        if patch is not None:
            self["hx-patch"] = patch
        if preserve is not None:
            self["hx-preserve"] = preserve
        if prompt is not None:
            self["hx-prompt"] = prompt
        if put is not None:
            self["hx-put"] = put
        if replace_url is not None:
            self["hx-replace-url"] = replace_url
        if request is not None:
            self["hx-request"] = request
        if sync is not None:
            self["hx-sync"] = sync
        if validate is not None:
            self["hx-validate"] = validate
        return self
