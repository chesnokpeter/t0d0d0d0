from abc import abstractmethod
from typing import Any
from .base import BaseRepo, sT
from ..entities import AddProject
from ..models import ProjectModel

class AbsProjectRepo(BaseRepo[sT]):

    @abstractmethod
    async def add(self, data: AddProject) -> ProjectModel: raise NotImplementedError

    @abstractmethod
    async def get(self, key: Any) -> ProjectModel | None: raise NotImplementedError

    @abstractmethod
    async def get_all(self, **data) -> list[ProjectModel] | None: raise NotImplementedError

    @abstractmethod
    async def update(self, key: Any, data: AddProject) -> ProjectModel: raise NotImplementedError

    @abstractmethod
    async def delete(self, key: Any) -> None: raise NotImplementedError

