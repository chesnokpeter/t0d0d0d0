from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from contextvars import ContextVar
from .base import AbsACIDConnector

def get_async_conn_postgres(postgres_url: str) -> async_sessionmaker:
    engine = create_async_engine(postgres_url)
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class PostgresConnector(AbsACIDConnector[async_sessionmaker]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._session_var = ContextVar[AsyncSession](f'session_{id(self)}', default=None)

    async def connect(self):
        session = self._session_var.get()
        if not session:
            session = self.maker()
            self._session_var.set(session)
        return session

    async def commit(self):
        session = self._session_var.get()
        if session:
            await session.commit()

    async def rollback(self):
        session = self._session_var.get()
        if session:
            await session.rollback()

    async def close(self):
        session = self._session_var.get()
        if session:
            await session.close()
            self._session_var.set(None)

    @property
    def session(self):
        session = self._session_var.get()
        if not session:
            raise RuntimeError("session not connected")
        return session
    
