from collections.abc import Collection
from ._elements import Content, SpecificContent, HTMLElement


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class head(HTMLElement):
    EMPTY = False
    TAG = "head"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class body(HTMLElement):
    EMPTY = False
    TAG = "body"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class html(HTMLElement):
    EMPTY = False
    TAG = "html"

    def __init__(
        self,
        *args: SpecificContent[head | body],
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: SpecificContent[head | body]) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class map(HTMLElement):  # pylint: disable=redefined-builtin
    EMPTY = False
    TAG = "map"

    def __init__(
        self,
        *args: Content,
        name: str | None = None,
        usemap: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if name is not None:
            self["name"] = name
        if usemap is not None:
            self["usemap"] = usemap
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class area(HTMLElement):
    EMPTY = True
    TAG = "area"

    def __init__(
        self,
        alt: str | None = None,
        coords: str | None = None,
        shape: str | None = None,
        href: str | None = None,
        target: str | None = None,
        download: str | None = None,
        ping: str | None = None,
        rel: str | None = None,
        referrerpolicy: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if alt is not None:
            self["alt"] = alt
        if coords is not None:
            self["coords"] = coords
        if shape is not None:
            self["shape"] = shape
        if href is not None:
            self["href"] = href
        if target is not None:
            self["target"] = target
        if download is not None:
            self["download"] = download
        if ping is not None:
            self["ping"] = ping
        if rel is not None:
            self["rel"] = rel
        if referrerpolicy is not None:
            self["referrerpolicy"] = referrerpolicy
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class article(HTMLElement):
    EMPTY = False
    TAG = "article"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class section(HTMLElement):
    EMPTY = False
    TAG = "section"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class nav(HTMLElement):
    EMPTY = False
    TAG = "nav"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class aside(HTMLElement):
    EMPTY = False
    TAG = "aside"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class h1(HTMLElement):
    EMPTY = False
    TAG = "h1"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class h2(HTMLElement):
    EMPTY = False
    TAG = "h2"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class h3(HTMLElement):
    EMPTY = False
    TAG = "h3"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class h4(HTMLElement):
    EMPTY = False
    TAG = "h4"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class h5(HTMLElement):
    EMPTY = False
    TAG = "h5"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class h6(HTMLElement):
    EMPTY = False
    TAG = "h6"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class hgroup(HTMLElement):
    EMPTY = False
    TAG = "hgroup"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class header(HTMLElement):
    EMPTY = False
    TAG = "header"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class footer(HTMLElement):
    EMPTY = False
    TAG = "footer"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class address(HTMLElement):
    EMPTY = False
    TAG = "address"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class picture(HTMLElement):
    EMPTY = False
    TAG = "picture"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class source(HTMLElement):
    EMPTY = True
    TAG = "source"

    def __init__(
        self,
        type: str | None = None,  # pylint: disable=redefined-builtin
        media: str | None = None,
        src: str | None = None,
        srcset: str | None = None,
        sizes: str | None = None,
        width: str | None = None,
        height: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if type is not None:
            self["type"] = type
        if media is not None:
            self["media"] = media
        if src is not None:
            self["src"] = src
        if srcset is not None:
            self["srcset"] = srcset
        if sizes is not None:
            self["sizes"] = sizes
        if width is not None:
            self["width"] = width
        if height is not None:
            self["height"] = height
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class img(HTMLElement):
    EMPTY = True
    TAG = "img"

    def __init__(
        self,
        alt: str | None = None,
        src: str | None = None,
        srcset: str | None = None,
        sizes: str | None = None,
        crossorigin: str | None = None,
        usemap: str | None = None,
        ismap: str | None = None,
        width: str | None = None,
        height: str | None = None,
        referrerpolicy: str | None = None,
        decoding: str | None = None,
        loading: str | None = None,
        fetchpriority: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if alt is not None:
            self["alt"] = alt
        if src is not None:
            self["src"] = src
        if srcset is not None:
            self["srcset"] = srcset
        if sizes is not None:
            self["sizes"] = sizes
        if crossorigin is not None:
            self["crossorigin"] = crossorigin
        if usemap is not None:
            self["usemap"] = usemap
        if ismap is not None:
            self["ismap"] = ismap
        if width is not None:
            self["width"] = width
        if height is not None:
            self["height"] = height
        if referrerpolicy is not None:
            self["referrerpolicy"] = referrerpolicy
        if decoding is not None:
            self["decoding"] = decoding
        if loading is not None:
            self["loading"] = loading
        if fetchpriority is not None:
            self["fetchpriority"] = fetchpriority
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class title(HTMLElement):
    EMPTY = False
    TAG = "title"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class base(HTMLElement):
    EMPTY = True
    TAG = "base"

    def __init__(
        self,
        href: str | None = None,
        target: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if href is not None:
            self["href"] = href
        if target is not None:
            self["target"] = target
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class link(HTMLElement):
    EMPTY = True
    TAG = "link"

    def __init__(
        self,
        href: str | None = None,
        crossorigin: str | None = None,
        rel: str | None = None,
        media: str | None = None,
        integrity: str | None = None,
        hreflang: str | None = None,
        type: str | None = None,  # pylint: disable=redefined-builtin
        referrerpolicy: str | None = None,
        sizes: str | None = None,
        imagesrcset: str | None = None,
        imagesizes: str | None = None,
        as_: str | None = None,
        blocking: str | None = None,
        color: str | None = None,
        disabled: bool | None = None,
        fetchpriority: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if href is not None:
            self["href"] = href
        if crossorigin is not None:
            self["crossorigin"] = crossorigin
        if rel is not None:
            self["rel"] = rel
        if media is not None:
            self["media"] = media
        if integrity is not None:
            self["integrity"] = integrity
        if hreflang is not None:
            self["hreflang"] = hreflang
        if type is not None:
            self["type"] = type
        if referrerpolicy is not None:
            self["referrerpolicy"] = referrerpolicy
        if sizes is not None:
            self["sizes"] = sizes
        if imagesrcset is not None:
            self["imagesrcset"] = imagesrcset
        if imagesizes is not None:
            self["imagesizes"] = imagesizes
        if as_ is not None:
            self["as"] = as_
        if blocking is not None:
            self["blocking"] = blocking
        if color is not None:
            self["color"] = color
        if disabled is not None:
            self["disabled"] = disabled
        if fetchpriority is not None:
            self["fetchpriority"] = fetchpriority
        if title is not None:
            self["title"] = title
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class meta(HTMLElement):
    EMPTY = True
    TAG = "meta"

    def __init__(
        self,
        name: str | None = None,
        http_equiv: str | None = None,
        content: str | None = None,
        charset: str | None = None,
        media: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if name is not None:
            self["name"] = name
        if http_equiv is not None:
            self["http-equiv"] = http_equiv
        if content is not None:
            self["content"] = content
        if charset is not None:
            self["charset"] = charset
        if media is not None:
            self["media"] = media
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class style(HTMLElement):
    EMPTY = False
    TAG = "style"

    def __init__(
        self,
        *args: str,
        media: str | None = None,
        blocking: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        translate: str | None = None,
        writingsuggestions: str | None = None,
        scoped: bool | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if media is not None:
            self["media"] = media
        if blocking is not None:
            self["blocking"] = blocking
        if title is not None:
            self["title"] = title
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        if scoped is not None:
            self["scoped"] = scoped
        self(*args)

    def __call__(self, *args: str) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class iframe(HTMLElement):
    EMPTY = True
    TAG = "iframe"

    def __init__(
        self,
        src: str | None = None,
        srcdoc: str | None = None,
        name: str | None = None,
        sandbox: str | None = None,
        allow: str | None = None,
        allowfullscreen: bool | None = None,
        width: str | None = None,
        height: str | None = None,
        referrerpolicy: str | None = None,
        loading: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if src is not None:
            self["src"] = src
        if srcdoc is not None:
            self["srcdoc"] = srcdoc
        if name is not None:
            self["name"] = name
        if sandbox is not None:
            self["sandbox"] = sandbox
        if allow is not None:
            self["allow"] = allow
        if allowfullscreen is not None:
            self["allowfullscreen"] = allowfullscreen
        if width is not None:
            self["width"] = width
        if height is not None:
            self["height"] = height
        if referrerpolicy is not None:
            self["referrerpolicy"] = referrerpolicy
        if loading is not None:
            self["loading"] = loading
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class embed(HTMLElement):
    EMPTY = True
    TAG = "embed"

    def __init__(
        self,
        src: str | None = None,
        type: str | None = None,  # pylint: disable=redefined-builtin
        width: str | None = None,
        height: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if src is not None:
            self["src"] = src
        if type is not None:
            self["type"] = type
        if width is not None:
            self["width"] = width
        if height is not None:
            self["height"] = height
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class object(HTMLElement):  # pylint: disable=redefined-builtin
    EMPTY = False
    TAG = "object"

    def __init__(
        self,
        *args: Content,
        data: str | None = None,  # pylint: disable=redefined-outer-name
        type: str | None = None,  # pylint: disable=redefined-builtin
        name: str | None = None,
        form: str | None = None,  # pylint: disable=redefined-outer-name
        width: str | None = None,
        height: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if data is not None:
            self["data"] = data
        if type is not None:
            self["type"] = type
        if name is not None:
            self["name"] = name
        if form is not None:
            self["form"] = form
        if width is not None:
            self["width"] = width
        if height is not None:
            self["height"] = height
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class table(HTMLElement):
    EMPTY = False
    TAG = "table"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class caption(HTMLElement):
    EMPTY = False
    TAG = "caption"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class colgroup(HTMLElement):
    EMPTY = True
    TAG = "colgroup"

    def __init__(
        self,
        span: str | None = None,  # pylint: disable=redefined-outer-name
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if span is not None:
            self["span"] = span
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class col(HTMLElement):
    EMPTY = True
    TAG = "col"

    def __init__(
        self,
        span: str | None = None,  # pylint: disable=redefined-outer-name
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if span is not None:
            self["span"] = span
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class tbody(HTMLElement):
    EMPTY = False
    TAG = "tbody"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class thead(HTMLElement):
    EMPTY = False
    TAG = "thead"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class tfoot(HTMLElement):
    EMPTY = False
    TAG = "tfoot"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class tr(HTMLElement):
    EMPTY = False
    TAG = "tr"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class td(HTMLElement):
    EMPTY = False
    TAG = "td"

    def __init__(
        self,
        *args: Content,
        colspan: str | None = None,
        rowspan: str | None = None,
        headers: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if colspan is not None:
            self["colspan"] = colspan
        if rowspan is not None:
            self["rowspan"] = rowspan
        if headers is not None:
            self["headers"] = headers
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class th(HTMLElement):
    EMPTY = False
    TAG = "th"

    def __init__(
        self,
        *args: Content,
        colspan: str | None = None,
        rowspan: str | None = None,
        headers: str | None = None,
        scope: str | None = None,
        abbr: str | None = None,  # pylint: disable=redefined-outer-name
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if colspan is not None:
            self["colspan"] = colspan
        if rowspan is not None:
            self["rowspan"] = rowspan
        if headers is not None:
            self["headers"] = headers
        if scope is not None:
            self["scope"] = scope
        if abbr is not None:
            self["abbr"] = abbr
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class input(HTMLElement):  # pylint: disable=redefined-builtin
    EMPTY = True
    TAG = "input"

    def __init__(
        self,
        accept: str | None = None,
        alt: str | None = None,
        autocomplete: str | None = None,
        checked: bool | None = None,
        dirname: str | None = None,
        disabled: bool | None = None,
        form: str | None = None,  # pylint: disable=redefined-outer-name
        formaction: str | None = None,
        formenctype: str | None = None,
        formmethod: str | None = None,
        formnovalidate: bool | None = None,
        formtarget: str | None = None,
        height: str | None = None,
        list: str | None = None,  # pylint: disable=redefined-builtin
        max: str | None = None,  # pylint: disable=redefined-builtin
        maxlength: str | None = None,
        min: str | None = None,  # pylint: disable=redefined-builtin
        minlength: str | None = None,
        multiple: bool | None = None,
        name: str | None = None,
        pattern: str | None = None,
        placeholder: str | None = None,
        popovertarget: str | None = None,
        popovertargetaction: str | None = None,
        readonly: bool | None = None,
        required: bool | None = None,
        size: str | None = None,
        src: str | None = None,
        step: str | None = None,
        type: str | None = None,  # pylint: disable=redefined-builtin
        value: str | None = None,
        width: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accept is not None:
            self["accept"] = accept
        if alt is not None:
            self["alt"] = alt
        if autocomplete is not None:
            self["autocomplete"] = autocomplete
        if checked is not None:
            self["checked"] = checked
        if dirname is not None:
            self["dirname"] = dirname
        if disabled is not None:
            self["disabled"] = disabled
        if form is not None:
            self["form"] = form
        if formaction is not None:
            self["formaction"] = formaction
        if formenctype is not None:
            self["formenctype"] = formenctype
        if formmethod is not None:
            self["formmethod"] = formmethod
        if formnovalidate is not None:
            self["formnovalidate"] = formnovalidate
        if formtarget is not None:
            self["formtarget"] = formtarget
        if height is not None:
            self["height"] = height
        if list is not None:
            self["list"] = list
        if max is not None:
            self["max"] = max
        if maxlength is not None:
            self["maxlength"] = maxlength
        if min is not None:
            self["min"] = min
        if minlength is not None:
            self["minlength"] = minlength
        if multiple is not None:
            self["multiple"] = multiple
        if name is not None:
            self["name"] = name
        if pattern is not None:
            self["pattern"] = pattern
        if placeholder is not None:
            self["placeholder"] = placeholder
        if popovertarget is not None:
            self["popovertarget"] = popovertarget
        if popovertargetaction is not None:
            self["popovertargetaction"] = popovertargetaction
        if readonly is not None:
            self["readonly"] = readonly
        if required is not None:
            self["required"] = required
        if size is not None:
            self["size"] = size
        if src is not None:
            self["src"] = src
        if step is not None:
            self["step"] = step
        if type is not None:
            self["type"] = type
        if value is not None:
            self["value"] = value
        if width is not None:
            self["width"] = width
        if title is not None:
            self["title"] = title
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class form(HTMLElement):
    EMPTY = False
    TAG = "form"

    def __init__(
        self,
        *args: Content,
        accept_charset: str | None = None,
        action: str | None = None,
        autocomplete: str | None = None,
        enctype: str | None = None,
        method: str | None = None,
        name: str | None = None,
        novalidate: bool | None = None,
        target: str | None = None,
        rel: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accept_charset is not None:
            self["accept-charset"] = accept_charset
        if action is not None:
            self["action"] = action
        if autocomplete is not None:
            self["autocomplete"] = autocomplete
        if enctype is not None:
            self["enctype"] = enctype
        if method is not None:
            self["method"] = method
        if name is not None:
            self["name"] = name
        if novalidate is not None:
            self["novalidate"] = novalidate
        if target is not None:
            self["target"] = target
        if rel is not None:
            self["rel"] = rel
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class label(HTMLElement):
    EMPTY = False
    TAG = "label"

    def __init__(
        self,
        *args: Content,
        for_: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if for_ is not None:
            self["for"] = for_
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class details(HTMLElement):
    EMPTY = False
    TAG = "details"

    def __init__(
        self,
        *args: Content,
        name: str | None = None,
        open: bool | None = None,  # pylint: disable=redefined-builtin
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if name is not None:
            self["name"] = name
        if open is not None:
            self["open"] = open
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class summary(HTMLElement):
    EMPTY = False
    TAG = "summary"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class dialog(HTMLElement):
    EMPTY = False
    TAG = "dialog"

    def __init__(
        self,
        *args: Content,
        open: bool | None = None,  # pylint: disable=redefined-builtin
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if open is not None:
            self["open"] = open
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class a(HTMLElement):
    EMPTY = False
    TAG = "a"

    def __init__(
        self,
        *args: Content,
        href: str | None = None,
        target: str | None = None,
        download: str | None = None,
        ping: str | None = None,
        rel: str | None = None,
        hreflang: str | None = None,
        type: str | None = None,  # pylint: disable=redefined-builtin
        referrerpolicy: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if href is not None:
            self["href"] = href
        if target is not None:
            self["target"] = target
        if download is not None:
            self["download"] = download
        if ping is not None:
            self["ping"] = ping
        if rel is not None:
            self["rel"] = rel
        if hreflang is not None:
            self["hreflang"] = hreflang
        if type is not None:
            self["type"] = type
        if referrerpolicy is not None:
            self["referrerpolicy"] = referrerpolicy
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class em(HTMLElement):
    EMPTY = False
    TAG = "em"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class strong(HTMLElement):
    EMPTY = False
    TAG = "strong"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class small(HTMLElement):
    EMPTY = False
    TAG = "small"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class s(HTMLElement):
    EMPTY = False
    TAG = "s"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class cite(HTMLElement):
    EMPTY = False
    TAG = "cite"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class q(HTMLElement):
    EMPTY = False
    TAG = "q"

    def __init__(
        self,
        *args: Content,
        cite: str | None = None,  # pylint: disable=redefined-outer-name
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if cite is not None:
            self["cite"] = cite
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class dfn(HTMLElement):
    EMPTY = False
    TAG = "dfn"

    def __init__(
        self,
        *args: Content,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if title is not None:
            self["title"] = title
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class abbr(HTMLElement):
    EMPTY = False
    TAG = "abbr"

    def __init__(
        self,
        *args: Content,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if title is not None:
            self["title"] = title
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class ruby(HTMLElement):
    EMPTY = False
    TAG = "ruby"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class rt(HTMLElement):
    EMPTY = False
    TAG = "rt"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class rp(HTMLElement):
    EMPTY = False
    TAG = "rp"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class data(HTMLElement):
    EMPTY = False
    TAG = "data"

    def __init__(
        self,
        *args: Content,
        value: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if value is not None:
            self["value"] = value
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class time(HTMLElement):
    EMPTY = False
    TAG = "time"

    def __init__(
        self,
        *args: Content,
        datetime: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if datetime is not None:
            self["datetime"] = datetime
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class code(HTMLElement):
    EMPTY = False
    TAG = "code"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class var(HTMLElement):
    EMPTY = False
    TAG = "var"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class samp(HTMLElement):
    EMPTY = False
    TAG = "samp"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class kbd(HTMLElement):
    EMPTY = False
    TAG = "kbd"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class sup(HTMLElement):
    EMPTY = False
    TAG = "sup"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class sub(HTMLElement):
    EMPTY = False
    TAG = "sub"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class i(HTMLElement):
    EMPTY = False
    TAG = "i"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class b(HTMLElement):
    EMPTY = False
    TAG = "b"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class u(HTMLElement):
    EMPTY = False
    TAG = "u"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class mark(HTMLElement):
    EMPTY = False
    TAG = "mark"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class bdi(HTMLElement):
    EMPTY = False
    TAG = "bdi"

    def __init__(
        self,
        *args: Content,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if dir is not None:
            self["dir"] = dir
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class bdo(HTMLElement):
    EMPTY = False
    TAG = "bdo"

    def __init__(
        self,
        *args: Content,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if dir is not None:
            self["dir"] = dir
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class span(HTMLElement):
    EMPTY = False
    TAG = "span"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class br(HTMLElement):
    EMPTY = True
    TAG = "br"

    def __init__(
        self,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class wbr(HTMLElement):
    EMPTY = True
    TAG = "wbr"

    def __init__(
        self,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class p(HTMLElement):
    EMPTY = False
    TAG = "p"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class hr(HTMLElement):
    EMPTY = True
    TAG = "hr"

    def __init__(
        self,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class pre(HTMLElement):
    EMPTY = False
    TAG = "pre"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class blockquote(HTMLElement):
    EMPTY = False
    TAG = "blockquote"

    def __init__(
        self,
        *args: Content,
        cite: str | None = None,  # pylint: disable=redefined-outer-name
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if cite is not None:
            self["cite"] = cite
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class ol(HTMLElement):
    EMPTY = False
    TAG = "ol"

    def __init__(
        self,
        *args: Content,
        reversed: bool | None = None,  # pylint: disable=redefined-builtin
        start: str | None = None,
        type: str | None = None,  # pylint: disable=redefined-builtin
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if reversed is not None:
            self["reversed"] = reversed
        if start is not None:
            self["start"] = start
        if type is not None:
            self["type"] = type
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class ul(HTMLElement):
    EMPTY = False
    TAG = "ul"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class menu(HTMLElement):
    EMPTY = False
    TAG = "menu"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class li(HTMLElement):
    EMPTY = False
    TAG = "li"

    def __init__(
        self,
        *args: Content,
        value: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if value is not None:
            self["value"] = value
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class dl(HTMLElement):
    EMPTY = False
    TAG = "dl"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class dt(HTMLElement):
    EMPTY = False
    TAG = "dt"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class dd(HTMLElement):
    EMPTY = False
    TAG = "dd"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class figure(HTMLElement):
    EMPTY = False
    TAG = "figure"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class figcaption(HTMLElement):
    EMPTY = False
    TAG = "figcaption"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class main(HTMLElement):
    EMPTY = False
    TAG = "main"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class search(HTMLElement):
    EMPTY = False
    TAG = "search"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class div(HTMLElement):
    EMPTY = False
    TAG = "div"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class video(HTMLElement):
    EMPTY = False
    TAG = "video"

    def __init__(
        self,
        *args: Content,
        src: str | None = None,
        crossorigin: str | None = None,
        poster: str | None = None,
        preload: str | None = None,
        autoplay: bool | None = None,
        playsinline: bool | None = None,
        loop: bool | None = None,
        muted: bool | None = None,
        controls: bool | None = None,
        width: str | None = None,
        height: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if src is not None:
            self["src"] = src
        if crossorigin is not None:
            self["crossorigin"] = crossorigin
        if poster is not None:
            self["poster"] = poster
        if preload is not None:
            self["preload"] = preload
        if autoplay is not None:
            self["autoplay"] = autoplay
        if playsinline is not None:
            self["playsinline"] = playsinline
        if loop is not None:
            self["loop"] = loop
        if muted is not None:
            self["muted"] = muted
        if controls is not None:
            self["controls"] = controls
        if width is not None:
            self["width"] = width
        if height is not None:
            self["height"] = height
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class audio(HTMLElement):
    EMPTY = False
    TAG = "audio"

    def __init__(
        self,
        *args: Content,
        src: str | None = None,
        crossorigin: str | None = None,
        preload: str | None = None,
        autoplay: bool | None = None,
        loop: bool | None = None,
        muted: bool | None = None,
        controls: bool | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if src is not None:
            self["src"] = src
        if crossorigin is not None:
            self["crossorigin"] = crossorigin
        if preload is not None:
            self["preload"] = preload
        if autoplay is not None:
            self["autoplay"] = autoplay
        if loop is not None:
            self["loop"] = loop
        if muted is not None:
            self["muted"] = muted
        if controls is not None:
            self["controls"] = controls
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class track(HTMLElement):
    EMPTY = True
    TAG = "track"

    def __init__(
        self,
        kind: str | None = None,
        src: str | None = None,
        srclang: str | None = None,
        label: str | None = None,  # pylint: disable=redefined-outer-name
        default: bool | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if kind is not None:
            self["kind"] = kind
        if src is not None:
            self["src"] = src
        if srclang is not None:
            self["srclang"] = srclang
        if label is not None:
            self["label"] = label
        if default is not None:
            self["default"] = default
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class ins(HTMLElement):
    EMPTY = False
    TAG = "ins"

    def __init__(
        self,
        *args: Content,
        cite: str | None = None,  # pylint: disable=redefined-outer-name
        datetime: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if cite is not None:
            self["cite"] = cite
        if datetime is not None:
            self["datetime"] = datetime
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class del_(HTMLElement):
    EMPTY = False
    TAG = "del"

    def __init__(
        self,
        *args: Content,
        cite: str | None = None,  # pylint: disable=redefined-outer-name
        datetime: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if cite is not None:
            self["cite"] = cite
        if datetime is not None:
            self["datetime"] = datetime
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class script(HTMLElement):
    EMPTY = False
    TAG = "script"

    def __init__(
        self,
        *args: str,
        src: str | None = None,
        type: str | None = None,  # pylint: disable=redefined-builtin
        nomodule: bool | None = None,
        async_: bool | None = None,
        defer: bool | None = None,
        crossorigin: str | None = None,
        integrity: str | None = None,
        referrerpolicy: str | None = None,
        blocking: str | None = None,
        fetchpriority: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if src is not None:
            self["src"] = src
        if type is not None:
            self["type"] = type
        if nomodule is not None:
            self["nomodule"] = nomodule
        if async_ is not None:
            self["async"] = async_
        if defer is not None:
            self["defer"] = defer
        if crossorigin is not None:
            self["crossorigin"] = crossorigin
        if integrity is not None:
            self["integrity"] = integrity
        if referrerpolicy is not None:
            self["referrerpolicy"] = referrerpolicy
        if blocking is not None:
            self["blocking"] = blocking
        if fetchpriority is not None:
            self["fetchpriority"] = fetchpriority
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: str) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class noscript(HTMLElement):
    EMPTY = False
    TAG = "noscript"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class template(HTMLElement):
    EMPTY = True
    TAG = "template"

    def __init__(
        self,
        shadowrootmode: str | None = None,
        shadowrootdelegatesfocus: bool | None = None,
        shadowrootclonable: bool | None = None,
        shadowrootserializable: bool | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if shadowrootmode is not None:
            self["shadowrootmode"] = shadowrootmode
        if shadowrootdelegatesfocus is not None:
            self["shadowrootdelegatesfocus"] = shadowrootdelegatesfocus
        if shadowrootclonable is not None:
            self["shadowrootclonable"] = shadowrootclonable
        if shadowrootserializable is not None:
            self["shadowrootserializable"] = shadowrootserializable
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class slot(HTMLElement):
    EMPTY = False
    TAG = "slot"

    def __init__(
        self,
        *args: Content,
        name: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if name is not None:
            self["name"] = name
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class button(HTMLElement):
    EMPTY = False
    TAG = "button"

    def __init__(
        self,
        *args: Content,
        disabled: bool | None = None,
        form: str | None = None,  # pylint: disable=redefined-outer-name
        formaction: str | None = None,
        formenctype: str | None = None,
        formmethod: str | None = None,
        formnovalidate: bool | None = None,
        formtarget: str | None = None,
        name: str | None = None,
        popovertarget: str | None = None,
        popovertargetaction: str | None = None,
        type: str | None = None,  # pylint: disable=redefined-builtin
        value: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if disabled is not None:
            self["disabled"] = disabled
        if form is not None:
            self["form"] = form
        if formaction is not None:
            self["formaction"] = formaction
        if formenctype is not None:
            self["formenctype"] = formenctype
        if formmethod is not None:
            self["formmethod"] = formmethod
        if formnovalidate is not None:
            self["formnovalidate"] = formnovalidate
        if formtarget is not None:
            self["formtarget"] = formtarget
        if name is not None:
            self["name"] = name
        if popovertarget is not None:
            self["popovertarget"] = popovertarget
        if popovertargetaction is not None:
            self["popovertargetaction"] = popovertargetaction
        if type is not None:
            self["type"] = type
        if value is not None:
            self["value"] = value
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class select(HTMLElement):
    EMPTY = False
    TAG = "select"

    def __init__(
        self,
        *args: Content,
        autocomplete: str | None = None,
        disabled: bool | None = None,
        form: str | None = None,  # pylint: disable=redefined-outer-name
        multiple: bool | None = None,
        name: str | None = None,
        required: bool | None = None,
        size: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if autocomplete is not None:
            self["autocomplete"] = autocomplete
        if disabled is not None:
            self["disabled"] = disabled
        if form is not None:
            self["form"] = form
        if multiple is not None:
            self["multiple"] = multiple
        if name is not None:
            self["name"] = name
        if required is not None:
            self["required"] = required
        if size is not None:
            self["size"] = size
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class datalist(HTMLElement):
    EMPTY = False
    TAG = "datalist"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class optgroup(HTMLElement):
    EMPTY = False
    TAG = "optgroup"

    def __init__(
        self,
        *args: Content,
        disabled: bool | None = None,
        label: str | None = None,  # pylint: disable=redefined-outer-name
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if disabled is not None:
            self["disabled"] = disabled
        if label is not None:
            self["label"] = label
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class option(HTMLElement):
    EMPTY = True
    TAG = "option"

    def __init__(
        self,
        disabled: bool | None = None,
        label: str | None = None,  # pylint: disable=redefined-outer-name
        selected: bool | None = None,
        value: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if disabled is not None:
            self["disabled"] = disabled
        if label is not None:
            self["label"] = label
        if selected is not None:
            self["selected"] = selected
        if value is not None:
            self["value"] = value
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class textarea(HTMLElement):
    EMPTY = False
    TAG = "textarea"

    def __init__(
        self,
        *args: str,
        autocomplete: str | None = None,
        cols: str | None = None,
        dirname: str | None = None,
        disabled: bool | None = None,
        form: str | None = None,  # pylint: disable=redefined-outer-name
        maxlength: str | None = None,
        minlength: str | None = None,
        name: str | None = None,
        placeholder: str | None = None,
        readonly: bool | None = None,
        required: bool | None = None,
        rows: str | None = None,
        wrap: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if autocomplete is not None:
            self["autocomplete"] = autocomplete
        if cols is not None:
            self["cols"] = cols
        if dirname is not None:
            self["dirname"] = dirname
        if disabled is not None:
            self["disabled"] = disabled
        if form is not None:
            self["form"] = form
        if maxlength is not None:
            self["maxlength"] = maxlength
        if minlength is not None:
            self["minlength"] = minlength
        if name is not None:
            self["name"] = name
        if placeholder is not None:
            self["placeholder"] = placeholder
        if readonly is not None:
            self["readonly"] = readonly
        if required is not None:
            self["required"] = required
        if rows is not None:
            self["rows"] = rows
        if wrap is not None:
            self["wrap"] = wrap
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: str) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class output(HTMLElement):
    EMPTY = False
    TAG = "output"

    def __init__(
        self,
        *args: Content,
        for_: str | None = None,
        form: str | None = None,  # pylint: disable=redefined-outer-name
        name: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if for_ is not None:
            self["for"] = for_
        if form is not None:
            self["form"] = form
        if name is not None:
            self["name"] = name
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class progress(HTMLElement):
    EMPTY = False
    TAG = "progress"

    def __init__(
        self,
        *args: Content,
        value: str | None = None,
        max: str | None = None,  # pylint: disable=redefined-builtin
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if value is not None:
            self["value"] = value
        if max is not None:
            self["max"] = max
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class meter(HTMLElement):
    EMPTY = False
    TAG = "meter"

    def __init__(
        self,
        *args: Content,
        value: str | None = None,
        min: str | None = None,  # pylint: disable=redefined-builtin
        max: str | None = None,  # pylint: disable=redefined-builtin
        low: str | None = None,
        high: str | None = None,
        optimum: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if value is not None:
            self["value"] = value
        if min is not None:
            self["min"] = min
        if max is not None:
            self["max"] = max
        if low is not None:
            self["low"] = low
        if high is not None:
            self["high"] = high
        if optimum is not None:
            self["optimum"] = optimum
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class fieldset(HTMLElement):
    EMPTY = False
    TAG = "fieldset"

    def __init__(
        self,
        *args: Content,
        disabled: str | None = None,
        form: str | None = None,  # pylint: disable=redefined-outer-name
        name: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if disabled is not None:
            self["disabled"] = disabled
        if form is not None:
            self["form"] = form
        if name is not None:
            self["name"] = name
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class legend(HTMLElement):
    EMPTY = False
    TAG = "legend"

    def __init__(
        self,
        *args: Content,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self


# noinspection PyPep8Naming,PyShadowingBuiltins,PyShadowingNames
class canvas(HTMLElement):
    EMPTY = False
    TAG = "canvas"

    def __init__(
        self,
        *args: Content,
        width: str | None = None,
        height: str | None = None,
        accesskey: str | None = None,
        autocapitalize: str | None = None,
        autocorrect: str | None = None,
        autofocus: bool | None = None,
        contenteditable: str | None = None,
        dir: str | None = None,  # pylint: disable=redefined-builtin
        draggable: str | None = None,
        enterkeyhint: str | None = None,
        hidden: str | None = None,
        inert: bool | None = None,
        inputmode: str | None = None,
        is_: str | None = None,
        itemid: str | None = None,
        itemprop: str | None = None,
        itemref: str | None = None,
        itemscope: bool | None = None,
        itemtype: str | None = None,
        lang: str | None = None,
        nonce: str | None = None,
        popover: str | None = None,
        spellcheck: str | None = None,
        class_: str | Collection[str] | None = None,
        style: str | None = None,  # pylint: disable=redefined-outer-name
        tabindex: str | None = None,
        title: str | None = None,  # pylint: disable=redefined-outer-name
        translate: str | None = None,
        writingsuggestions: str | None = None,
        **kwargs: str | bool | Collection[str] | None,
    ):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v
        if width is not None:
            self["width"] = width
        if height is not None:
            self["height"] = height
        if accesskey is not None:
            self["accesskey"] = accesskey
        if autocapitalize is not None:
            self["autocapitalize"] = autocapitalize
        if autocorrect is not None:
            self["autocorrect"] = autocorrect
        if autofocus is not None:
            self["autofocus"] = autofocus
        if contenteditable is not None:
            self["contenteditable"] = contenteditable
        if dir is not None:
            self["dir"] = dir
        if draggable is not None:
            self["draggable"] = draggable
        if enterkeyhint is not None:
            self["enterkeyhint"] = enterkeyhint
        if hidden is not None:
            self["hidden"] = hidden
        if inert is not None:
            self["inert"] = inert
        if inputmode is not None:
            self["inputmode"] = inputmode
        if is_ is not None:
            self["is"] = is_
        if itemid is not None:
            self["itemid"] = itemid
        if itemprop is not None:
            self["itemprop"] = itemprop
        if itemref is not None:
            self["itemref"] = itemref
        if itemscope is not None:
            self["itemscope"] = itemscope
        if itemtype is not None:
            self["itemtype"] = itemtype
        if lang is not None:
            self["lang"] = lang
        if nonce is not None:
            self["nonce"] = nonce
        if popover is not None:
            self["popover"] = popover
        if spellcheck is not None:
            self["spellcheck"] = spellcheck
        if class_ is not None:
            self["class"] = class_
        if style is not None:
            self["style"] = style
        if tabindex is not None:
            self["tabindex"] = tabindex
        if title is not None:
            self["title"] = title
        if translate is not None:
            self["translate"] = translate
        if writingsuggestions is not None:
            self["writingsuggestions"] = writingsuggestions
        self(*args)

    def __call__(self, *args: Content) -> HTMLElement:
        self._content.extend(args)
        return self
