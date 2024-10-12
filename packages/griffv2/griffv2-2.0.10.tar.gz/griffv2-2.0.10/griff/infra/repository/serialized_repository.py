from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from injector import inject

from griff.domain.common_types import Aggregate
from griff.infra.persistence.serialized_persistence import SerializedPersistence
from griff.infra.repository.repository import Repository
from griff.services.date.date_service import DateService

A = TypeVar("A", bound=Aggregate)


class SerializedRepository(Generic[A], Repository[A], ABC):
    @inject
    @abstractmethod
    def __init__(
        self,
        persistence: SerializedPersistence,
        date_service: DateService,
    ):
        super().__init__(persistence, date_service)
