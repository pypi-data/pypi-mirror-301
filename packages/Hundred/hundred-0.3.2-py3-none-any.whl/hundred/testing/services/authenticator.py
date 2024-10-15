from datetime import datetime
from typing import Any

import orjson
from injection.testing import test_singleton

from hundred.exceptions import Unauthorized
from hundred.gettext import gettext as _
from hundred.services.authenticator import StatelessAuthenticator
from hundred.services.datetime import DateTimeService
from hundred.services.hasher import Hasher


@test_singleton(on=StatelessAuthenticator, mode="fallback")
class InMemoryAuthenticator(StatelessAuthenticator):
    __slots__ = ("__datetime_service", "__hasher", "__tokens")

    def __init__(self, datetime_service: DateTimeService, hasher: Hasher):
        self.__datetime_service = datetime_service
        self.__hasher = hasher
        self.__tokens = dict[str, dict[str, Any]]()

    def generate_token(
        self,
        data: dict[str, Any],
        expiration: datetime | None = None,
    ) -> str:
        payload: dict[str, Any] = {"sub": data}

        if expiration:
            payload["exp"] = expiration.timestamp()

        token_json = orjson.dumps(payload).decode()
        token = self.__hasher.hash(token_json)
        self.__tokens[token] = payload
        return token

    def authenticate(self, token: str) -> dict[str, Any]:
        try:
            payload = self.__tokens[token]

        except KeyError:
            error_message = _("invalid_jwt")

        else:
            now = self.__datetime_service.utcnow().timestamp()
            expiration = payload.get("exp")

            if expiration is None or now < expiration:
                return payload["sub"]

            error_message = _("jwt_expired")

        raise Unauthorized(error_message)
