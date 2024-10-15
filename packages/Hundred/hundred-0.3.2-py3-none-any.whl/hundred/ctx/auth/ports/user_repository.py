from abc import abstractmethod
from typing import Protocol, runtime_checkable

from injection import should_be_injectable

from hundred.ctx.auth.domain import User


@should_be_injectable
@runtime_checkable
class UserRepository(Protocol):
    __slots__ = ()

    @abstractmethod
    async def get_by_identifier(self, identifier: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, user: User) -> None:
        raise NotImplementedError
