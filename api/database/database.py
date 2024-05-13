import asyncio
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from alembic.config import Config
from alembic import command

from api.settings import settings


engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True)
    input_value = Column(String, nullable=False)
    valid_input = Column(Boolean, default=0, nullable=False)
    execution_time = Column(DateTime, default=datetime.utcnow(), nullable=False)
    execute_duration = Column(Integer, default=0, nullable=False)
    images = Column(JSON)


# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)

# asyncio.run(init_models())