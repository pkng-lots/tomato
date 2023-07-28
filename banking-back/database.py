from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_DATABASE_URL = "postgresql+psycopg://postgres:password@localhost:5432/banking"

engine = create_engine(
    SQL_DATABASE_URL
)
SessionLocal = sessionmaker(engine)

Base = declarative_base()
