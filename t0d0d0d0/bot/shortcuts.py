from dishka.integrations.aiogram import FromDishka

from typing import Annotated, TypeVar, TypeAlias

from .ioc import SetupUOW



T = TypeVar('T')

UseCase: TypeAlias = Annotated[FromDishka[T], T]

SUOW: TypeAlias = Annotated[FromDishka[SetupUOW], SetupUOW]

