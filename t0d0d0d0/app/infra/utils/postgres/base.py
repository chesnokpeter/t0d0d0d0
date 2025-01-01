from abc import ABC, abstractmethod

class AbsPostgresTable(ABC):
    id: int
    @abstractmethod
    def model(self):
        raise NotImplementedError
