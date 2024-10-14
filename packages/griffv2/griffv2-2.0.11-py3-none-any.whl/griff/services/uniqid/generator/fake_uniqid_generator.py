from injector import singleton

from griff.services.uniqid.generator.uniqid_generator import UniqIdGenerator


@singleton
class FakeUniqIdGenerator(UniqIdGenerator):
    def __init__(self, start_id=1):
        self._start = 0
        self._start = start_id - 1

    def next_id(self) -> str:
        self._start = self._start + 1
        return self._format_id(self._start)

    def reset(self, start_id: int = 1):
        self._start = start_id - 1

    @staticmethod
    def _format_id(str_id: int) -> str:
        return f"FAKEULID{str_id:018d}"
