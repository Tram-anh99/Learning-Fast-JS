"""
========== Database Configuration ==========
File: config.py
Mục đích: Quản lý cấu hình ứng dụng từ environment variables (.env file)
Kết nối với: .env, database.py, app.py
=========================================
"""

# Import BaseSettings từ pydantic_settings để tạo class cấu hình
# Pydantic sẽ tự động đọc giá trị từ file .env
from pydantic_settings import BaseSettings

# Import lru_cache để cache settings instance (chỉ tạo 1 lần duy nhất)
from functools import lru_cache


class Settings(BaseSettings):
    """Class chứa tất cả cấu hình ứng dụng
    Pydantic sẽ tự động:
    - Đọc giá trị từ file .env
    - Validate kiểu dữ liệu
    - Provide default values nếu không có trong .env
    """
    
    # ===== DATABASE CONFIGURATION =====
    # Các thông tin kết nối PostgreSQL database
    
    DB_HOST: str = "localhost"      # Địa chỉ server PostgreSQL (mặc định: localhost)
    DB_PORT: int = 5433             # Port PostgreSQL (mặc định: 5433, không phải 5432 mặc định)
    DB_NAME: str = "postgres"       # Tên database
    DB_USER: str = "postgres"       # Username để đăng nhập
    DB_PASSWORD: str = "123456"     # Password (có thể thử 000000 nếu không đúng)
    DB_SCHEMA: str = "nongsan"      # Schema name chứa các bảng của app
    
    # ===== API CONFIGURATION =====
    # Các cấu hình cho FastAPI application
    
    API_TITLE: str = "Agriculture Management API"  # Tiêu đề hiển thị trong API docs
    API_VERSION: str = "2.0.0"                      # Phiên bản API
    API_PREFIX: str = "/api"                        # Prefix cho tất cả routes (vd: /api/farms)
    
    # ===== CORS CONFIGURATION =====
    # Cross-Origin Resource Sharing - cho phép frontend gọi API
    # Format: string với các URL cách nhau bằng dấu phẩy
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:5174,http://localhost:3000"
    # 5173: Vite dev server (mặc định)
    # 5174: Vite dev server backup
    # 3000: React/Next.js dev server
    
    @property
    def cors_origins_list(self) -> list:
        """Property method để convert string CORS_ORIGINS thành list
        
        Ví dụ:
            Input: "http://localhost:5173,http://localhost:5174"
            Output: ["http://localhost:5173", "http://localhost:5174"]
        
        Returns:
            list: Danh sách các origin được phép
        """
        # Split string theo dấu phẩy, strip() để loại bỏ khoảng trắng
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def DATABASE_URL(self) -> str:
        """
        Property method để tạo PostgreSQL connection string
        
        Format: postgresql://user:password@host:port/database
        Example: postgresql://postgres:123456@localhost:5432/postgres
        
        Kết nối đến:
        - database.py: create_engine(settings.DATABASE_URL)
        - SQLAlchemy engine
        
        Returns:
            str: Connection URL string
        """
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def DATABASE_URL_ASYNC(self) -> str:
        """
        Property method để tạo async PostgreSQL connection string
        
        Format: postgresql+asyncpg://user:password@host:port/database
        Note: Dùng asyncpg driver thay vì psycopg2 (cho async operations)
        
        Usage: Nếu sau này migrate sang async SQLAlchemy
        
        Returns:
            str: Async connection URL string
        """
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        """
        Pydantic config class
        
        Attributes:
        - env_file: Tên file chứa environment variables (.env)
        - extra: Allow thêm fields không define trong class ("allow" = ignore extra fields)
        """
        env_file = ".env"      # Đọc config từ file .env
        extra = "allow"        # Cho phép thêm fields không được định nghĩa


# ========== SETTINGS INSTANCE ==========

@lru_cache()
def get_settings() -> Settings:
    """
    Factory function để tạo Settings instance (với caching)
    
    Cách hoạt động:
    1. @lru_cache() decorator cache kết quả function
    2. Lần đầu gọi: Tạo Settings instance mới, cache lại
    3. Các lần sau: Return instance đã cache (không tạo mới)
    
    Benefits:
    - Chỉ đọc .env file 1 lần duy nhất
    - Tiết kiệm memory (singleton pattern)
    - Thread-safe
    
    Returns:
        Settings: Cached settings instance
    
    Kết nối đến:
    - app.py: from config import settings
    - database.py: from config import settings
    - routes/*.py: from config import settings
    """
    return Settings()


# Global settings instance
# Import và dùng: from config import settings
settings = get_settings()
