from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from prova_mp_i.config.settings import settings, PROJECT_ROOT


class Config:

    @staticmethod
    def get_database_url():
        if settings.DATABASE_TYPE == 'sqlite':
            return f'sqlite:///{PROJECT_ROOT}/database.db'
        if settings.DATABASE_TYPE == 'postgresql':
            return f'postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'
        raise ValueError("Invalid database type. ('sqlite', 'postgresql')")


engine = create_engine(Config.get_database_url(), echo=False,
                       connect_args={'check_same_thread': False} if settings.DATABASE_TYPE == 'sqlite' else {})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
