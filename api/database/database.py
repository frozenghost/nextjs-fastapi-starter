from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "postgresql://root:BOpQjE99ra5g@localhost/chatbot"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    input_value = Column(String)
    valid_input = Column(Boolean)
    execution_time = Column(DateTime, default=datetime.now)
    images = Column(String)

Base.metadata.create_all(bind=engine)