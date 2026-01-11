from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create engine based on database type
if DATABASE_URL.startswith("postgresql"):
    # For PostgreSQL/Neon
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "sslmode": "require",
        },
        pool_recycle=300,
        pool_pre_ping=True,
    )
else:
    # For SQLite (fallback for development)
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get a database session
    """
    with Session(engine) as session:
        yield session