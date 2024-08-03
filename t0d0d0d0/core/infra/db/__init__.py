from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

def asyncfactory_postgres(postgres_url: str) -> async_sessionmaker:
    engine = create_async_engine(postgres_url)
    get_async_conn_postgres = async_sessionmaker(engine, expire_on_commit=False)
    return get_async_conn_postgres

