"""Initial migration: create users and tasks tables using SQLModel metadata.

This migration uses SQLModel.metadata.create_all for initial schema creation to
keep the migration simple and aligned with the models defined in
`api/todo/models.py`.
"""

from sqlmodel import SQLModel
from todo.db import engine


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create all tables."""
    SQLModel.metadata.create_all(engine)


def downgrade() -> None:
    """Drop all tables."""
    SQLModel.metadata.drop_all(engine)
