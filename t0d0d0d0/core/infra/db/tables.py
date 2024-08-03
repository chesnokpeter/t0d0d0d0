from datetime import datetime, date, time
from sqlalchemy import inspect, BigInteger, ForeignKey, DateTime, Integer, String, Enum, Date, Time
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from abc import ABC, abstractmethod
from t0d0d0d0.core.infra.db.models import UserModel, ProjectModel, TaskModel
from t0d0d0d0.core.infra.db.enums import TaskStatus


class AbsMODEL(ABC):
    id: int
    @abstractmethod
    def model(self): raise NotImplementedError


class Base(DeclarativeBase):
    def __repr__(self):
        mapper = inspect(self).mapper
        ent = []
        for col in [*mapper.column_attrs]:
            ent.append("{0}={1}".format(col.key, getattr(self, col.key)))
        return "<{0}(".format(self.__class__.__name__) + ", ".join(ent) + ")>"


class USER(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer(), unique=True, primary_key=True, autoincrement=True, nullable=False)
    tgid: Mapped[int] = mapped_column(BigInteger(), nullable=False)
    tgusername: Mapped[str] = mapped_column(String(), nullable=False)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    
    tasks: Mapped[list['TASK']] = relationship("TASK", back_populates="user", cascade="all, delete-orphan", lazy="subquery")
    projects: Mapped[list['PROJECT']] = relationship("PROJECT", back_populates="user", cascade="all, delete-orphan", lazy="subquery")
    
    def model(self):
        return UserModel(
            id=self.id,
            tgid=self.tgid,
            tgusername=self.tgusername,
            name=self.name,
            # tasks=self.tasks,
            # projects=self.projects
        )


class TASK(Base):
    __tablename__ = "task"
    id: Mapped[int] = mapped_column(Integer(), unique=True, primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    createdat: Mapped[datetime] = mapped_column(DateTime(), nullable=False, default=datetime.now())
    date: Mapped['date'] = mapped_column(Date(), nullable=True)
    time: Mapped['time'] = mapped_column(Time(), nullable=True)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), nullable=False, default=TaskStatus.backlog)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("project.id"), nullable=True)

    user: Mapped['USER'] = relationship("USER", back_populates="tasks", lazy="subquery")
    project: Mapped['PROJECT'] = relationship("PROJECT", back_populates="tasks", lazy="subquery")
    
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
            # user=self.user,
            # project=self.project
        )


class PROJECT(Base):
    __tablename__ = "project"
    id: Mapped[int] = mapped_column(Integer(), unique=True, primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    createdat: Mapped[datetime] = mapped_column(DateTime(), nullable=False, default=datetime.now())
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)

    user: Mapped['USER'] = relationship("USER", back_populates="projects", lazy="subquery")
    tasks: Mapped[list['TASK']] = relationship("TASK", back_populates="project", cascade="all, delete-orphan", lazy="subquery")
    
    def model(self):
        return ProjectModel(
            id=self.id,
            name=self.name,
            createdat=self.createdat,
            user_id=self.user_id,
            # tasks=self.tasks
        )