from abc import abstractmethod
from datetime import datetime
from typing import Any, ClassVar, Protocol, runtime_checkable

from injection import should_be_injectable
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWT

from hundred.exceptions import Unauthorized
from hundred.gettext import gettext as _


@should_be_injectable
@runtime_checkable
class StatelessAuthenticator(Protocol):
    __slots__ = ()

    @abstractmethod
    def generate_token(
        self,
        data: dict[str, Any],
        expiration: datetime | None = ...,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def authenticate(self, token: str) -> dict[str, Any]:
        raise NotImplementedError


class JWTAuthenticator(StatelessAuthenticator):
    __slots__ = ("__secret_key",)

    __algorithm: ClassVar[str] = "HS256"
    __jwt: ClassVar[PyJWT] = PyJWT(options={"require": ["sub"]})

    def __init__(self, secret_key: str) -> None:
        self.__secret_key = secret_key

    def generate_token(
        self,
        data: dict[str, Any],
        expiration: datetime | None = None,
    ) -> str:
        payload: dict[str, Any] = {"sub": data}

        if expiration:
            payload["exp"] = expiration.timestamp()

        return self.__jwt.encode(
            payload=payload,
            key=self.__secret_key,
            algorithm=self.__algorithm,
        )

    def authenticate(self, token: str) -> dict[str, Any]:
        try:
            payload: dict[str, Any] = self.__jwt.decode(
                jwt=token,
                key=self.__secret_key,
                algorithms=[self.__algorithm],
            )

        except ExpiredSignatureError:
            error_message = _("jwt_expired")

        except InvalidTokenError:
            error_message = _("invalid_jwt")

        else:
            return payload["sub"]

        raise Unauthorized(error_message)
