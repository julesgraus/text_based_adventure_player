from abc import ABC, abstractmethod


class Rule(ABC):
    @abstractmethod
    def is_valid(self, value) -> bool:
        pass

    @abstractmethod
    def message(self, attribute: str, value) -> str:
        pass
