from abc import ABC
from typing import TypeVar, Generic

from ...shared import RepoDependsOnRegister

TSESION = TypeVar('T')


class BaseRepo(ABC, Generic[TSESION], metaclas=RepoDependsOnRegister):
    depends_on: str

    def connect(self, session: TSESION):
        self.session = session
