from datetime import date as datetype
from datetime import datetime
from datetime import time as timetype

from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Time,
    inspect,
)
from sqlalchemy import Enum as ORMEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from t0d0d0d0.coreback.infra.abstract import DbAbsTable
from t0d0d0d0.coreback.models.enums import TaskStatus
from t0d0d0d0.coreback.models.project import ProjectModel
from t0d0d0d0.coreback.models.task import TaskModel
from t0d0d0d0.coreback.models.user import UserModel


class Base(DeclarativeBase):
    def __repr__(self):
        mapper = inspect(self).mapper
        ent = []
        for col in [*mapper.column_attrs]:
            ent.append('{0}={1}'.format(col.key, getattr(self, col.key)))
        return '<{0}('.format(self.__class__.__name__) + ', '.join(ent) + ')>'


class USER(Base, DbAbsTable):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(
        Integer(),
        unique=True,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    tgid: Mapped[int] = mapped_column(BigInteger(), nullable=False)
    tgusername: Mapped[str] = mapped_column(String(), nullable=False)
    name: Mapped[str] = mapped_column(String(), nullable=False)

    aes_private_key: Mapped[str] = mapped_column(String(), nullable=False)
    public_key: Mapped[str] = mapped_column(String(), nullable=False)

    tasks: Mapped[list['TASK']] = relationship(
        'TASK',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='subquery',
    )
    projects: Mapped[list['PROJECT']] = relationship(
        'PROJECT',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='subquery',
    )

    def model(self):
        return UserModel(
            id=self.id,
            tgid=self.tgid,
            tgusername=self.tgusername,
            name=self.name,
            aes_private_key=self.aes_private_key,
            public_key=self.public_key
        )


class TASK(Base, DbAbsTable):
    __tablename__ = 'task'
    id: Mapped[int] = mapped_column(
        Integer(),
        unique=True,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(), nullable=False)
    createdat: Mapped[datetime] = mapped_column(DateTime(), nullable=False, default=datetime.now())
    date: Mapped[datetype] = mapped_column(Date(), nullable=True)
    time: Mapped[timetype] = mapped_column(Time(), nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        ORMEnum(TaskStatus), nullable=False, default=TaskStatus.backlog
    )

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('project.id', ondelete='CASCADE'), nullable=True
    )

    user: Mapped['USER'] = relationship('USER', back_populates='tasks', lazy='subquery')
    project: Mapped['PROJECT'] = relationship('PROJECT', back_populates='tasks', lazy='subquery')

    def model(self):
        return TaskModel(
            id=self.id,
            name=self.name,
            createdat=self.createdat,
            date=self.date,
            time=self.time,
            status=self.status,
            user_id=self.user_id,
            project_id=self.project_id,
        )


class PROJECT(Base, DbAbsTable):
    __tablename__ = 'project'
    id: Mapped[int] = mapped_column(
        Integer(),
        unique=True,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(), nullable=False)
    createdat: Mapped[datetime] = mapped_column(DateTime(), nullable=False, default=datetime.now())

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)

    user: Mapped['USER'] = relationship('USER', back_populates='projects', lazy='subquery')
    tasks: Mapped[list['TASK']] = relationship(
        'TASK',
        back_populates='project',
        cascade='all, delete-orphan',
        lazy='subquery',
    )

    def model(self):
        return ProjectModel(
            id=self.id,
            name=self.name,
            createdat=self.createdat,
            user_id=self.user_id,
        )
