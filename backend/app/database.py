"""Database engine and session factory."""

import os
from collections.abc import Generator
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Load .env from the backend folder (stable regardless of current working directory).
_BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(_BACKEND_DIR / ".env")

_default_sqlite_path = (_BACKEND_DIR / "banking.db").as_posix()
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{_default_sqlite_path}")

# SQLite needs check_same_thread=False when used with multiple threads (e.g. FastAPI).
connect_args: dict = {}
engine_kwargs: dict = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    # Avoid stale connections after idle timeouts (typical with PostgreSQL).
    engine_kwargs["pool_pre_ping"] = True

engine = create_engine(DATABASE_URL, connect_args=connect_args, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency-style session for APIs; yields a session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
