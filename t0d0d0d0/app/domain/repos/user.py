from abc import ABC, abstractmethod
from typing import Any

from ..entities import AddUser
from ..models import UserModel

class AbsUserRepo(ABC):

    @abstractmethod
    async def add(self, data: AddUser) -> UserModel: raise NotImplementedError

    @abstractmethod
    async def get(self, key: Any) -> UserModel | None: raise NotImplementedError

    @abstractmethod
    async def get_all(self, **data) -> list[UserModel] | None: raise NotImplementedError

    @abstractmethod
    async def update(self, key: Any, data: AddUser) -> UserModel: raise NotImplementedError

