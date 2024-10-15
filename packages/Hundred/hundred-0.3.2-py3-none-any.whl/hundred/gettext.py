from injection import inject

from hundred.services.i18n import I18NService

__all__ = ("gettext",)


@inject
def gettext(msgid: str, service: I18NService = ..., /) -> str:
    return service.get_translations().gettext(msgid)
