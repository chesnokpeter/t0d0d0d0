from t0d0d0d0.coreback.models.abstract import MemoryAbsModel, DbAbsModel, BrokerAbsModel, AbsModel

from typing import TypeAlias, Any, TypeVar, Generic, Type

AbsSession: TypeAlias = Any

TSESSION = TypeVar('TSESSION', bound=AbsSession)

class AbsRepo(Generic[TSESSION]):
    model: AbsModel
    reponame: str

    def __init__(self, require_connector: str):
        self.require_connector = require_connector

    def __call__(self, session: TSESSION) -> AbsModel:
        self.session = session

class MemoryAbsRepo(AbsRepo[TSESSION]):
    model: MemoryAbsModel
    def get(self): raise NotImplementedError
    def add(self): raise NotImplementedError
    def delete(self): raise NotImplementedError

class BrokerAbsRepo(AbsRepo[TSESSION]):
    model: BrokerAbsModel
    def send(self): raise NotImplementedError

class DbAbsRepo(AbsRepo[TSESSION]):
    model: DbAbsModel
    async def get(self): raise NotImplementedError
    async def get_one(self): raise NotImplementedError
    async def add(self): raise NotImplementedError
    async def offset(self): raise NotImplementedError
    async def update(self): raise NotImplementedError
    async def delete(self): raise NotImplementedError