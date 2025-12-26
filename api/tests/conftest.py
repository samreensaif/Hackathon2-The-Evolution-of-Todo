import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from todo.main import app
from todo.db import engine as prod_engine

# Use in-memory SQLite for testing
sqlite_url = "sqlite://"


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        sqlite_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    # We need to override the engine in todo.db or use a different approach.
    # For simplicity in this scaffold, we'll patch the engine in the modules.
    import todo.db
    import todo.routes.tasks
    import todo.routes.auth

    old_engine = todo.db.engine
    todo.db.engine = session.bind  # session.bind is the engine
    todo.routes.tasks.engine = session.bind
    todo.routes.auth.engine = session.bind

    client = TestClient(app)
    yield client

    todo.db.engine = old_engine
    todo.routes.tasks.engine = old_engine
    todo.routes.auth.engine = old_engine
