import inspect
import random
from abc import ABC
from decimal import Decimal
from typing import Self, List

from griff.domain.common_types import Entity
from griff.infra.persistence.persistence import Persistence
from griff.infra.repository.repository import Repository
from griff.services.date.fake_date_service import FakeDateService
from griff.services.service_locator.service_locator import ServiceLocator
from griff.services.uniqid.uniqid_service import UniqIdService


class DataTestFactory(ABC):
    def __init__(self, start_id=1):
        self.uniqid_service = ServiceLocator.get(UniqIdService)
        self.date_service = FakeDateService()
        self._sequence = {}
        random.seed(42)
        self._random_state = random.getstate()
        self.reset(start_id)
        self._created = {}

    def reset(self, start_id=1):
        self.uniqid_service.reset(start_id)

    async def persist(
        self, repository: Repository, data: list[Entity] | Entity
    ) -> Self:
        if isinstance(data, list) is False:
            await repository.save(data)
            return self

        for a in data:
            await repository.save(a)
        return self

    async def persist_by_persistence(
        self, persistence: Persistence, data: List[Entity] | Entity
    ) -> Self:
        initial_data = data if isinstance(data, list) else [data]
        prepared_data = [d.model_dump() for d in initial_data]
        persistence.reset(initial_data=prepared_data)
        return self

    def _random_decimal(self, min, max) -> Decimal:
        random.setstate(self._random_state)
        min = float(min) * 100
        max = float(max) * 100
        val = Decimal(random.uniform(min, max)) / 100
        self._random_state = random.getstate()
        return val

    def _random_int(self, min, max) -> int:
        random.setstate(self._random_state)
        val = random.randrange(min, max)
        self._random_state = random.getstate()
        return val

    def _next_sequence(self):
        current_frame = inspect.currentframe()
        calling_frame = inspect.getouterframes(current_frame, 2)
        caller = calling_frame[1][3]
        if caller not in self._sequence:
            self._sequence[caller] = 0
        self._sequence[caller] += 1
        # self.uniqid_service.reset(self._sequence[caller])
        return self._sequence[caller]

    def _add_created(self, name, created):
        if name not in self._created:
            self._created[name] = []
        self._created[name].append(created)
        return created

    def list_created(self, name):
        return self._created[name] if name in self._created else []
