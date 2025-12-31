"""
========== Database Connection ==========
Kết nối và quản lý PostgreSQL với SQLAlchemy

Module này quản lý:
- Kết nối đến PostgreSQL database
- Tạo engine và session factory
- Cung cấp database session cho FastAPI routes
- Test kết nối và lấy thông tin schema

Dependencies:
- config.py: Lấy cấu hình database từ environment
- SQLAlchemy: ORM framework cho Python
"""

# Import thư viện SQLAlchemy để quản lý database
from sqlalchemy import create_engine, text  # create_engine: tạo kết nối DB, text: viết raw SQL
from sqlalchemy.orm import sessionmaker, Session  # sessionmaker: factory tạo session, Session: type hint
from sqlalchemy.ext.declarative import declarative_base  # Base class cho tất cả models
from contextlib import contextmanager  # Decorator để tạo context manager (with statement)
from config import settings  # Import cấu hình từ config.py (DATABASE_URL, DB_SCHEMA, etc.)
import logging  # Thư viện logging để ghi log

# ========== SETUP LOGGING ==========
# Cấu hình logging ở mức INFO để xem thông tin kết nối
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # Tạo logger với tên module hiện tại

# ========== TẠO DATABASE ENGINE ==========
# Engine là điểm kết nối chính đến database
# Mọi thao tác với DB đều thông qua engine này
engine = create_engine(
    settings.DATABASE_URL,  # URL kết nối: postgresql://user:password@host:port/database
    pool_size=10,           # Số connection tối đa trong pool (10 connections sẵn sàng)
    max_overflow=20,        # Số connection thêm có thể tạo khi pool đầy (tối đa 30 total)
    pool_pre_ping=True,     # Kiểm tra connection trước khi dùng (tránh lỗi timeout)
    connect_args={"options": f"-c search_path={settings.DB_SCHEMA}"}  # Set schema mặc định là 'nongsan'
)

# ========== TẠO SESSION FACTORY ==========
# SessionLocal là factory function để tạo database session
# Mỗi request HTTP sẽ có 1 session riêng, đảm bảo isolation
SessionLocal = sessionmaker(
    autocommit=False,  # Không tự động commit (phải gọi db.commit() thủ công)
    autoflush=False,   # Không tự động flush changes vào DB (kiểm soát tốt hơn)
    bind=engine        # Liên kết với engine đã tạo ở trên
)

# ========== TẠO BASE CLASS CHO MODELS ==========
# Base là class cha cho tất cả ORM models
# Mọi model (Vung, SanPham, etc.) sẽ kế thừa từ Base này
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
