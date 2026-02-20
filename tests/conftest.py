from __future__ import annotations

import os
import tempfile
import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import create_app, API_PREFIX
from app.db.base import Base
from app.db import session as session_module

@pytest.fixture(scope="session")
def db_url():
    # Use file-based sqlite for stability across threads
    fd, path = tempfile.mkstemp(prefix="test_db_", suffix=".sqlite")
    os.close(fd)
    return f"sqlite:///{path}"

@pytest.fixture()
def client(db_url):
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

    Base.metadata.create_all(bind=engine)

    # Override dependency
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app = create_app()
    app.dependency_overrides[session_module.get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    Base.metadata.drop_all(bind=engine)
