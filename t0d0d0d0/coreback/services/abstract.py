from abc import ABC
from typing import Annotated, TypeAlias
from t0d0d0d0.coreback.uow import UnitOfWork, ALLRepoUnitOfWork

UnitOfWork: TypeAlias = Annotated[ALLRepoUnitOfWork, UnitOfWork]


class AbsService(ABC):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

