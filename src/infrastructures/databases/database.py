from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config.config import get_config



DATABASE_URL = "postgresql+psycopg2://{username}:{password}@{host}:{port}/{name}".format(
    **get_config().database['belajar'].__dict__
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def postgres(name: str) -> Session:
    engine = create_engine(
        "postgresql+psycopg2://{username}:{password}@{host}:{port}/{name}".format(
            **get_config().database[name].__dict__
        )
    )
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = session_local()
    return db

