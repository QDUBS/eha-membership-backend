from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import environ as env


# DATABASE_URL = "postgresql://postgres:mypostgresqlpassword@0.0.0.0:5432/eha-membership"
DATABASE_URL = "postgresql://postgres:mypostgresqlpassword@host.docker.internal:5432/eha-membership"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
