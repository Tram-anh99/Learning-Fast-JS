"""
========== Database Connection ==========
Kết nối và quản lý PostgreSQL với SQLAlchemy
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from config import settings
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    connect_args={"options": f"-c search_path={settings.DB_SCHEMA}"}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency để inject database session vào routes
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """Context manager cho database session"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def test_connection() -> bool:
    """Kiểm tra kết nối database"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("✅ Database connection successful!")
            return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False


def get_table_count() -> dict:
    """Đếm số bảng trong schema"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = '{settings.DB_SCHEMA}'
            """))
            tables = [row[0] for row in result]
            return {"schema": settings.DB_SCHEMA, "tables": tables, "count": len(tables)}
    except Exception as e:
        logger.error(f"Error getting table count: {e}")
        return {"error": str(e)}


# Test connection on module load
if __name__ == "__main__":
    test_connection()
    print(get_table_count())
