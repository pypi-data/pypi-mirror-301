from abc import ABC
from typing import Any

from hundred.gettext import gettext as _


class HundredError(Exception, ABC): ...


class HundredStatusError(HundredError, ABC):
    __slots__ = ("status_code", "details")

    def __init__(
        self,
        message: str,
        *,
        status_code: int = 400,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.details = details

    def dump(self) -> dict[str, Any]:
        if details := self.details:
            return details

        return {"message": str(self)}


class NotModified(HundredStatusError):
    def __init__(self, target: str) -> None:
        super().__init__(
            _("not_modified").format(target=target),
            status_code=304,
        )


class Unauthorized(HundredStatusError):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(
            message or _("unauthorized"),
            status_code=401,
        )


class Forbidden(HundredStatusError):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(
            message or _("forbidden"),
            status_code=403,
        )


class NotFound(HundredStatusError):
    def __init__(self, target: str) -> None:
        super().__init__(
            _("not_found").format(target=target),
            status_code=404,
        )


class Conflict(HundredStatusError):
    def __init__(self, target: str) -> None:
        super().__init__(
            _("conflict").format(target=target),
            status_code=409,
        )
