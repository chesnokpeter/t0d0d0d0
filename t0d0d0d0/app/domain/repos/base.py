from abc import ABC

from typing import TypeVar, Generic

TSESION = TypeVar('T')


class BaseRepo(ABC, Generic[TSESION]):
    def __init__(self, session: TSESION):
        self.session = session
