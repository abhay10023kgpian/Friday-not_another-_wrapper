
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

load_dotenv()

# -------------------------------------------------------------
# Read-Only Engine for LLM / Text-to-SQL (SELECT ONLY)
# -------------------------------------------------------------
READONLY_DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{os.getenv('DB_READONLY_USER', 'llm_user')}:{os.getenv('DB_READONLY_PASSWORD')}"
    f"@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}"
    f"/{os.getenv('DB_NAME', 'ragdb')}"
)

ADMIN_DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{os.getenv('DB_USER', 'abhay')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}"
    f"/{os.getenv('DB_NAME', 'ragdb')}"
)

readonly_engine = create_engine(
    READONLY_DATABASE_URL,
    pool_pre_ping=True
)

admin_engine = create_engine(
    ADMIN_DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=admin_engine
)

Base = declarative_base()


# Dependency for getting database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_connection():
    """Context manager for raw SQL connection with auto-cleanup."""
    conn = readonly_engine.connect()
    try:
        yield conn
    except Exception as e:
        print(f"Error during database operation: {e}")
        raise
    finally:
        conn.close()