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


# ========== DEPENDENCY INJECTION CHO FASTAPI ==========
def get_db():
    """
    Dependency function để inject database session vào FastAPI routes
    
    Cách hoạt động:
    1. Tạo session mới từ SessionLocal()
    2. Yield session cho route sử dụng (route nhận được db instance)
    3. Sau khi route xử lý xong, tự động đóng session (cleanup)
    
    Usage trong route:
    @app.get("/api/farms/")
    def get_farms(db: Session = Depends(get_db)):
        farms = db.query(Vung).all()  # Sử dụng db session ở đây
        return farms  # FastAPI tự động close db sau khi return
    
    Kết nối đến:
    - routes/*.py: Tất cả routes import và dùng Depends(get_db)
    - SessionLocal (line 37): Factory tạo session
    """
    db = SessionLocal()  # Tạo session mới từ factory
    try:
        yield db  # Trả session cho route, đợi route xử lý xong
    finally:
        db.close()  # Đảm bảo đóng session dù có lỗi hay không


# ========== CONTEXT MANAGER CHO DATABASE SESSION ==========
@contextmanager
def get_db_context():
    """
    Context manager để sử dụng database session với 'with' statement
    
    Cách hoạt động:
    1. Tạo session khi vào block 'with'
    2. Tự động commit nếu không có lỗi
    3. Rollback nếu có exception
    4. Luôn đóng session khi thoát block
    
    Usage:
    with get_db_context() as db:
        farm = db.query(Vung).filter(Vung.id == 1).first()
        farm.ten_vung = "New Name"
        # Tự động commit khi thoát khỏi with block
    
    Khác với get_db():
    - get_db(): Dùng với FastAPI Depends (auto injection)
    - get_db_context(): Dùng với 'with' statement (manual usage)
    
    Kết nối đến:
    - Có thể dùng trong scripts, tests, hoặc background tasks
    - SessionLocal (line 37): Factory tạo session
    """
    db = SessionLocal()  # Tạo session mới
    try:
        yield db              # Trả session cho code block
        db.commit()           # Commit transaction nếu thành công
    except Exception as e:
        db.rollback()         # Rollback nếu có lỗi
        raise e               # Re-raise exception để caller xử lý
    finally:
        db.close()            # Luôn đóng session


# ========== TEST CONNECTION FUNCTION ==========
def test_connection() -> bool:
    """
    Kiểm tra kết nối đến PostgreSQL database
    
    Cách hoạt động:
    1. Tạo connection từ engine
    2. Chạy câu SQL đơn giản: "SELECT 1" (query test cơ bản)
    3. Log kết quả: Success ✅ hoặc Error ❌
    4. Return True/False để caller biết trạng thái
    
    Returns:
        bool: True nếu kết nối thành công, False nếu lỗi
    
    Usage:
        if test_connection():
            print("Database ready!")
        else:
            print("Database not available")
    
    Kết nối đến:
    - engine (line 28): Sử dụng engine.connect() để tạo connection
    - config.py: DATABASE_URL được lấy từ settings
    """
    try:
        with engine.connect() as conn:  # Tạo connection (auto close khi thoát with)
            result = conn.execute(text("SELECT 1"))  # Execute raw SQL query
            logger.info("✅ Database connection successful!")  # Log success
            return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")  # Log error với message
        return False


# ========== GET TABLE COUNT FUNCTION ==========
def get_table_count() -> dict:
    """
    Đếm số bảng (tables) trong schema PostgreSQL
    
    Cách hoạt động:
    1. Query bảng information_schema.tables (metadata của PostgreSQL)
    2. Filter theo schema name (mặc định: 'nongsan')
    3. Lấy danh sách tên bảng và đếm số lượng
    4. Return dictionary với schema name, danh sách bảng, và count
    
    Returns:
        dict: {
            "schema": "nongsan",
            "tables": ["vung", "san_pham", "nhat_ky", ...],
            "count": 18
        }
        hoặc {"error": "error message"} nếu có lỗi
    
    Usage:
        info = get_table_count()
        print(f"Schema {info['schema']} has {info['count']} tables")
        print(f"Tables: {', '.join(info['tables'])}")
    
    Kết nối đến:
    - engine (line 28): Sử dụng engine.connect()
    - config.py: settings.DB_SCHEMA = "nongsan"
    - PostgreSQL system catalog: information_schema.tables
    """
    try:
        with engine.connect() as conn:  # Tạo connection
            # Query metadata từ PostgreSQL
            result = conn.execute(text(f"""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = '{settings.DB_SCHEMA}'
            """))
            # Convert ResultProxy thành list of table names
            tables = [row[0] for row in result]  # row[0] = table_name (cột đầu tiên)
            # Return thông tin đầy đủ
            return {
                "schema": settings.DB_SCHEMA,  # Schema name: "nongsan"
                "tables": tables,               # List tên bảng: ["vung", "san_pham", ...]
                "count": len(tables)            # Số lượng bảng: 18
            }
    except Exception as e:
        logger.error(f"Error getting table count: {e}")
        return {"error": str(e)}  # Return error message nếu có lỗi


# ========== MODULE INITIALIZATION ==========
# Test connection khi module được import (chỉ chạy nếu run trực tiếp)
if __name__ == "__main__":
    # Test kết nối database
    test_connection()
    # In ra số lượng bảng trong schema
    print(get_table_count())
