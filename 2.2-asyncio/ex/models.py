from sqlalchemy import JSON, Integer
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

PG_DNS = "postgresql+asyncpg://swapi:secret@localhost:5431/swapi_db"

engine = create_async_engine(PG_DNS)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class SwapiPeople(Base):
    __tablename__ = "swapi_people"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    json: Mapped[dict] = mapped_column(JSON)


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()
