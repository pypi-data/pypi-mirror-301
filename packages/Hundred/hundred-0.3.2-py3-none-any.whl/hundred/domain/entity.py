from abc import ABC
from typing import ClassVar, Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Entity(BaseModel, ABC):
    id: UUID = Field(frozen=True)

    model_config: ClassVar[ConfigDict] = ConfigDict(validate_assignment=True)


class Aggregate(Entity, ABC):
    version: int = Field(default=1, gt=0)

    @property
    def is_first_version(self) -> bool:
        return self.version == 1

    def bump_version(self) -> Self:
        self.version += 1
        return self

    def is_outdated(self, existing_version: int) -> bool:
        return existing_version != self.version - 1
