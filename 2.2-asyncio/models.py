from sqlalchemy import Integer, JSON
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import String
from dotenv import load_dotenv
load_dotenv()

PG_DSN = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    pass

class SwapiPeople(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    height: Mapped[str] = mapped_column(String)
    mass: Mapped[str] = mapped_column(String)
    hair_color: Mapped[str] = mapped_column(String)
    skin_color: Mapped[str] = mapped_column(String)
    eye_color: Mapped[str] = mapped_column(String)
    birth_year: Mapped[str] = mapped_column(String)
    gender: Mapped[str] = mapped_column(String)


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()