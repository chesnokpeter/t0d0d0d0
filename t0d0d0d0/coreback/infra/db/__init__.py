from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

def get_async_conn_postgres(postgres_url: str) -> async_sessionmaker:
    engine = create_async_engine(postgres_url)
    return async_sessionmaker(engine, expire_on_commit=False)

