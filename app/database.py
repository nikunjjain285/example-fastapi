from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from .config import settings

# SQLALCHEMY_DATABASE_URL =f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_server}/{settings.database_name}"
SQLALCHEMY_DATABASE_URL="postgresql://postgres:PLrisk%40123@localhost/fastapi"
engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,bind=engine,autoflush=False)

Base=declarative_base()

# Dependency
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()