from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


# Database engine and session factory
# This will be configured with DATABASE_URL environment variable
def get_engine(database_url: str) -> Engine:
    return create_engine(database_url)


def get_session_factory(engine: Engine) -> sessionmaker:
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
