from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_DATABASE_URL = "postgresql+psycopg://postgres:password@localhost:5432/banking"

# TODO: move to async engine.
engine = create_engine(
    SQL_DATABASE_URL
)
SessionLocal = sessionmaker(engine)

Base = declarative_base()
