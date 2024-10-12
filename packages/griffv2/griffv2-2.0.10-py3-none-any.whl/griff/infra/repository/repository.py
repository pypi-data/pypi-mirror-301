from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type

from injector import inject
from pydantic import ValidationError

from griff.domain.common_types import Entity
from griff.infra.persistence.dict_persistence import DictPersistence
from griff.infra.persistence.persistence import (
    Persistence,
    QueryRowResult,
)
from griff.services.date.date_service import DateService
from griff.utils.exceptions import EntityNotFoundException

A = TypeVar("A", bound=Entity)


class FakeRepositoryMixin:  # pragma: no cover
    _persistence: DictPersistence

    def reset(self):
        self._persistence.reset()


class Repository(Generic[A], ABC):
    @inject
    @abstractmethod
    def __init__(
        self,
        persistence: Persistence,
        date_service: DateService,
    ):
        self._date_service = date_service
        self._persistence = persistence

    async def get_by_id(self, entity_id: str) -> A | None:
        raw_data = await self._get_by_id(entity_id)
        if raw_data is not None:
            return self._hydrate_result(raw_data)

        raise EntityNotFoundException(
            f"Entity '{self._aggregate_class(raw_data)._entity_label()}' "
            f"(entity_id={entity_id}) not found"
        )

    async def save(self, aggregate: A) -> None:
        existing_entity = await self._get_by_id(aggregate.entity_id)
        prepared_data = aggregate.model_dump()
        if existing_entity is None:
            prepared_data = self._create_metadata(prepared_data)
            await self._persistence.insert(prepared_data)
            return None
        prepared_data = self._update_metadata(prepared_data)
        await self._persistence.update(prepared_data)
        return None

    async def delete(self, aggregate: A) -> None:
        await self.get_by_id(aggregate.entity_id)
        await self._persistence.delete(aggregate.entity_id)

    async def list_all(self) -> list[A]:
        raw_data = await self._persistence.list_all()
        return [self._hydrate_result(row) for row in raw_data if row]

    async def run_query(self, query_name: str, **query_params):
        raw_data = await self._persistence.run_query(query_name, **query_params)
        if raw_data is None:
            return None
        if isinstance(raw_data, list):
            return [self._hydrate_result(row) for row in raw_data if row]
        return self._hydrate_result(raw_data)

    async def _get_by_id(self, entity_id: str) -> dict | None:
        try:
            return await self._persistence.get_by_id(entity_id)
        except ValueError:
            return None

    def reset(self):  # pragma: no cover
        # Only for testing purpose
        pass

    def _hydrate_aggregate(self, raw_data: dict) -> A:
        aggregate_class = self._aggregate_class(raw_data)
        try:
            aggregate = aggregate_class.model_validate(raw_data)
        except ValidationError as e:
            raise RuntimeError(
                f"Data from persistence are not valid, hydratation "
                f"{aggregate_class._entity_label()} impossible : {e.errors()}"
            )

        return aggregate

    def _hydrate_result(self, result: QueryRowResult) -> A:
        return self._hydrate_aggregate(result)

    def _create_metadata(self, target: dict) -> dict:
        now = self._date_service.now().to_datetime()
        target["created_at"] = now
        target["updated_at"] = now
        return target

    def _update_metadata(self, target: dict) -> dict:
        # to be sure
        target.pop("created_at", None)
        target["updated_at"] = self._date_service.now().to_datetime()
        return target

    @staticmethod
    @abstractmethod
    def _aggregate_class(raw_data: dict | None = None) -> Type[A]:  # pragma: no cover
        ...
