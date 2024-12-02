from abc import ABC, abstractmethod
from typing import Any
from .base import BaseRepo
from ..entities import AddTask
from ..models import TaskModel

class AbsTaskRepo(BaseRepo, ABC):

    @abstractmethod
    async def add(self, data: AddTask) -> TaskModel: raise NotImplementedError

    @abstractmethod
    async def get(self, key: Any) -> TaskModel | None: raise NotImplementedError

    @abstractmethod
    async def get_all(self, **data) -> list[TaskModel] | None: raise NotImplementedError

    @abstractmethod
    async def update(self, key: Any, data: AddTask) -> TaskModel: raise NotImplementedError


