from abc import ABC

from typing import TypeVar, Generic

T = TypeVar('T')


class BaseRepo(ABC, Generic[T]):
    def __init__(self, session: T):
        self.session = session
