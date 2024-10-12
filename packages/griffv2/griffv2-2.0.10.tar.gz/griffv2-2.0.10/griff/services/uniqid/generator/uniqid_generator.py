import abc


class UniqIdGenerator(abc.ABC):
    @abc.abstractmethod
    def next_id(self) -> str:
        ...  # pragma: no cover

    @abc.abstractmethod
    def reset(self, start_id: int = 1) -> None:  # pragma: no cover
        pass
