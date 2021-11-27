from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
from .config import settings

SQL_ALCHEMY_DATABASE_URL = f"{settings.database_type}://{quote(settings.database_username)}:{quote(settings.database_password)}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
