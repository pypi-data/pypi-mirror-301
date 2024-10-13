from abc import ABC, abstractmethod

class Clause(ABC):
    @abstractmethod
    def build(self) -> str:
        ...
    
    @property
    @abstractmethod
    def place(self) -> int:
        ...

    @property
    def is_exclusive(self) -> bool:
        return True
