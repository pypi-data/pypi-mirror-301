from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TypeVar

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from ..interface.session import SessionProviderInterface
from ..models.model import DbBaseModel
from ..models.schema import BaseSchema

BaseDbModelType = TypeVar("BaseDbModelType", bound=DbBaseModel)
BaseSchemaType = TypeVar("BaseSchemaType", bound=BaseSchema)


class BaseCrudInterface(ABC):
    session_provider: SessionProviderInterface

    @abstractmethod
    async def create(
        self,
        instance: BaseSchema | Sequence[BaseSchema],
        *,
        exclude_fields: set | None = None,
        with_relations: bool = False,
        session: AsyncSession = None,
    ):
        ...

    @abstractmethod
    async def update(
        self,
        instance: BaseSchema | None = None,
        *,
        filters: dict | tuple[str, ...] | None = None,
        exclude_fields: tuple[str, ...] | None = None,
        update_fields: dict | tuple[str, ...] | None = None,
        session: AsyncSession | None = None,
    ) -> BaseSchema:
        ...

    @abstractmethod
    async def update_or_create(
        self,
        instance: BaseSchema,
        *,
        with_relations: bool = False,
        filters: dict | tuple[str, ...] | None = None,
        exclude_fields: tuple[str, ...] | None = None,
        update_fields: tuple[str, ...] | None = None,
        session: AsyncSession | None = None,
    ) -> tuple[bool, BaseSchemaType]:
        ...

    @abstractmethod
    async def update_many(
        self,
        update_data: dict,
        filters: dict,
        exclude_fields: tuple[str, ...] | None = None,
        session: AsyncSession | None = None,
    ) -> list[BaseSchemaType]:
        ...

    @abstractmethod
    async def get_or_none(
        self,
        filters: dict,
        *,
        session: AsyncSession | None = None,
        response_schema: BaseSchemaType = None,
    ) -> BaseSchemaType | None:
        ...

    @abstractmethod
    async def get(
        self,
        filters: dict,
        response_schema: BaseSchemaType = None,
        session: AsyncSession = None,
    ) -> BaseSchemaType:
        ...

    @abstractmethod
    async def all(
        self,
        response_schema: BaseSchemaType = None,
        session: AsyncSession | None = None,
    ) -> list[BaseSchemaType]:
        ...

    @abstractmethod
    async def filter(
        self,
        filters: dict,
        *,
        order: tuple[str, ...] = None,
        response_schema: BaseSchemaType = None,
        session: AsyncSession | None = None,
        limit: int = 0,
        offset: int = 0,
        sa_filters: tuple = None,
    ) -> list[BaseSchema]:
        ...

    @abstractmethod
    async def filter_statement(
        self,
        statement: Select,
        *,
        response_schema: BaseSchemaType = None,
        session: AsyncSession | None = None,
    ) -> list[BaseSchemaType]:
        ...

    @abstractmethod
    async def filter_statement_with_count(
        self,
        statement: Select,
        *,
        response_schema: BaseSchemaType = None,
        limit: int | None = None,
        offset: int | None = None,
        session: AsyncSession | None = None,
        count_stmt: Select | None = None,
        is_use_scalars: bool = True,
    ) -> tuple[int, list[BaseSchema]]:
        ...

    @abstractmethod
    async def filter_with_total_count(
        self,
        filters: dict,
        *,
        order: Sequence[str, ...] = None,
        response_schema: BaseSchemaType = None,
        session: AsyncSession | None = None,
        limit: int = 0,
        offset: int = 0,
        sa_filters: Sequence = None,
    ) -> (int, list[BaseSchema]):
        ...

    @abstractmethod
    async def delete(
        self, filters: dict, *, session: AsyncSession | None = None
    ) -> int:
        ...
