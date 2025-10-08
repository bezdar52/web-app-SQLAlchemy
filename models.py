from sqlalchemy import ForeignKey, String, BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine("sqlite+aiosqlite:///dbase.db")
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
  pass

class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True)
  tg_id = mapped_column(BigInteger)
  username: Mapped[str] = mapped_column(String(255))

class Task(Base):
  __tablename__ = "tasks"

  id: Mapped[int] = mapped_column(primary_key=True)
  title: Mapped[str] = mapped_column(String(255))
  completed: Mapped[bool] = mapped_column(default=False)
  user: Mapped[int] = mapped_column(ForeignKey("users.id"), ondelete="CASCADE")


async def init_db():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
