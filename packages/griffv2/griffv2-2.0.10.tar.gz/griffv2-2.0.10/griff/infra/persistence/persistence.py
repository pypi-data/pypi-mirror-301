from abc import ABC, abstractmethod
from typing import List, Any, Dict

QueryRowResult = Dict[str, Any]
QueryRowResults = List[QueryRowResult]
QueryResult = None | QueryRowResult | QueryRowResults


class Persistence(ABC):  # pragma: no cover
    async def insert(self, data: dict) -> None:
        prepared_data = self._prepare_to_save(data)
        return await self._insert(prepared_data)

    async def update(self, data: dict) -> None:
        prepared_data = self._prepare_to_save(data)
        return await self._update(prepared_data)

    async def delete(self, persistence_id: str) -> None:
        return await self._delete(persistence_id)

    async def get_by_id(self, persistence_id: str) -> QueryRowResult | None:
        result = await self._get_by_id(persistence_id)
        return self._prepare_row_result(result) if result else None

    async def list_all(self) -> QueryRowResults:
        results = await self._list_all()
        return self._prepare_row_results(results)

    async def run_query(self, query_name: str, **query_params) -> QueryResult:
        results = await self._run_query(query_name, **query_params)
        if isinstance(results, list):
            return self._prepare_row_results(results)
        return self._prepare_row_result(results) if results else None  # type: ignore

    @abstractmethod
    async def _insert(self, data: dict) -> None:
        ...

    @abstractmethod
    async def _update(self, data: dict) -> None:
        ...

    @abstractmethod
    async def _delete(self, persistence_id: str) -> None:
        ...

    @abstractmethod
    async def _get_by_id(self, persistence_id: str) -> QueryRowResult | None:
        ...

    @abstractmethod
    async def _list_all(self) -> QueryRowResults:
        ...

    @abstractmethod
    async def _run_query(self, query_name: str, **query_params) -> QueryResult:
        ...

    def reset(self, initial_data: List[Dict] | None = None):
        # only for testing purposes
        return None

    # noinspection PyMethodMayBeStatic
    def _prepare_to_save(self, data: dict) -> dict:
        return data

    # noinspection PyMethodMayBeStatic
    def _prepare_row_result(self, result: QueryRowResult) -> QueryRowResult:
        return result

    def _prepare_row_results(self, results: QueryRowResults) -> QueryRowResults:
        return [self._prepare_row_result(row) for row in results]
