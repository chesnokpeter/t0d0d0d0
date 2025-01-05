from abc import ABC
from typing import TypeVar, Generic

from ...shared import RepoDependsOnRegister

sT = TypeVar('T')

class NonSession:...


class BaseRepo(ABC, Generic[sT]):
    depends_on: str

    def connect(self, session: sT):
        self.session = session
