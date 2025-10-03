from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from digital_folder.core.config import project_settings


def get_db_url() -> str:
    env = project_settings.env.lower()
    db_url = {
        "dev": project_settings.dev_database_url,
        "prod": project_settings.prod_database_url,
    }

    if env not in db_url:
        raise ValueError(f"Invalid ENV value: {project_settings.env}.")

    return db_url[env]


# SQLAlchemy engine
engine = create_engine(str(get_db_url()), echo=project_settings.debug, future=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model class (used by models.py)
Base = declarative_base()


def get_db():
    from digital_folder.db.service import DbService

    with DbService() as db:
        yield db
