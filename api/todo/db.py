"""Database helper for Todo API (SQLModel engine + init helper)."""

import os
from sqlmodel import SQLModel, create_engine

# Read DB connection from env; default is a local Postgres placeholder.
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/todo_dev"
)

# create_engine uses SQLAlchemy URL; echo is off by default in production.
engine = create_engine(DATABASE_URL, echo=False)


def init_db() -> None:
    """Initialize DB by creating all tables from SQLModel metadata.

    Note: In production use Alembic migrations. This helper is useful for local
    dev and tests to bootstrap schema.
    """
    SQLModel.metadata.create_all(engine)
