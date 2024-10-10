from abc import ABC, abstractmethod


class JSONable(ABC):
    @abstractmethod
    def to_json(self) -> str:
        pass
