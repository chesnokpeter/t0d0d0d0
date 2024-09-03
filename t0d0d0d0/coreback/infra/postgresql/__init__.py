from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from t0d0d0d0.coreback.infra.abstract import AbsConnector

def get_async_conn_postgres(postgres_url: str) -> async_sessionmaker:
    engine = create_async_engine(postgres_url)
    return async_sessionmaker(engine, expire_on_commit=False)

class PostgresConnector(AbsConnector):
    def __init__(self, connector_name: str, postgres_url: str):
        self.maker = get_async_conn_postgres(postgres_url)
        self.connector_name = connector_name
    async def connect(self):
        self._session = self.maker()
    async def commit(self):
        self._session.commit()
    async def rollback(self):
        self._session.rollback()
    async def close(self):
        await self._session.close()
    @property
    def session(self):
        return self._session