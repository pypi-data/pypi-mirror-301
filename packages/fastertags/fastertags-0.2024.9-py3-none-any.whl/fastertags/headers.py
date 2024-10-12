class Header:
    key = ""

    def __init__(self, value: str) -> None:
        self._value: str = value

    @property
    def value(self) -> str:
        return self._value

    def __str__(self) -> str:
        return f"{self.key}: {self.value}"


class ContentType(Header):
    key = "Content-Type"


class HTMXHeader(Header):
    pass


class HXLocation(HTMXHeader):
    key = "HX-Location"


class HXPushUrl(HTMXHeader):
    key = "HX-Push-Url"


class HXRedirect(HTMXHeader):
    key = "HX-Redirect"


class HXRefresh(HTMXHeader):
    key = "HX-Refresh"


class HXReplaceUrl(HTMXHeader):
    key = "HX-Replace-Url"


class HXReswap(HTMXHeader):
    key = "HX-Reswap"


class HXRetarget(HTMXHeader):
    key = "HX-Retarget"


class HXReselect(HTMXHeader):
    key = "HX-Reselect"


class HXTrigger(HTMXHeader):
    key = "HX-Trigger"


class HXTriggerAfterSettle(HTMXHeader):
    key = "HX-Trigger-After-Settle"


class HXTriggerAfterSwap(HTMXHeader):
    key = "HX-Trigger-After-Swap"
