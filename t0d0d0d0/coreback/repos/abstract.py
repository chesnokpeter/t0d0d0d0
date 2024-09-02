from t0d0d0d0.coreback.models.abstract import MemoryAbsModel, DbAbsModel, BrokerAbsModel, AbsModel

class AbsRepo:
    model: AbsModel
    def __init__(self):...

class MemoryAbsRepo(AbsRepo):
    model: MemoryAbsModel
    def __init__(self): ...
    def get(self): raise NotImplementedError
    def add(self): raise NotImplementedError
    def delete(self): raise NotImplementedError

class BrokerAbsRepo(AbsRepo):
    model: BrokerAbsModel
    def __init__(self): ...
    def send(self): raise NotImplementedError

class DbAbsRepo(AbsRepo):
    model: DbAbsModel
    def __init__(self): ...
    async def get(self): raise NotImplementedError
    async def get_one(self): raise NotImplementedError
    async def add(self): raise NotImplementedError
    async def offset(self): raise NotImplementedError
    async def update(self): raise NotImplementedError
    async def delete(self): raise NotImplementedError