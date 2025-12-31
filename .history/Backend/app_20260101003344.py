"""
========== FastAPI Backend Application ==========
Purpose: API server cho ứng dụng quản lý nông nghiệp
Architecture: RESTful API với PostgreSQL database
Author: Learning-Fast-JS
Date: 2025-12-31 (Updated with PostgreSQL)

Module này:
- Khởi tạo FastAPI application
- Cấu hình CORS cho Frontend
- Include các route modules (farms, charts, diary)
- Cung cấp health check và root endpoints
- Khởi động Uvicorn server

Kết nối đến:
- config.py: Lấy cấu hình (API_TITLE, API_VERSION, CORS_ORIGINS)
- database.py: Test connection, get table count
- routes/farms.py: Farm/Vùng APIs
- routes/charts.py: Chart/Thống kê APIs
- routes/diary.py: Diary/Nhật ký APIs
"""

# Import FastAPI framework để tạo REST API
from fastapi import FastAPI  # Core FastAPI class
from fastapi.middleware.cors import CORSMiddleware  # Middleware xử lý CORS (Cross-Origin Resource Sharing)
import uvicorn  # ASGI server để chạy FastAPI app
import logging  # Thư viện logging để ghi log

# Import config and database modules
from config import settings  # Import cấu hình từ file config.py (API_TITLE, DATABASE_URL, etc.)
from database import test_connection, get_table_count  # Functions kiểm tra database

# Import route modules (mỗi module handle 1 nhóm endpoints)
from routes import farms   # Farms/Vùng APIs: CRUD operations cho vùng trồng
from routes import charts  # Charts/Thống kê APIs: Lấy dữ liệu cho biểu đồ
from routes import diary   # Diary/Nhật ký APIs: Quản lý nhật ký hoạt động

# ========== SETUP LOGGING ==========
# Cấu hình logging format và level
logging.basicConfig(
    level=logging.INFO,  # Log level: INFO (log mọi thứ từ INFO trở lên: INFO, WARNING, ERROR)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Format: timestamp - logger_name - level - message
)
logger = logging.getLogger(__name__)  # Tạo logger cho module này (__name__ = "app")

# ========== INITIALIZE FASTAPI APPLICATION ==========
# Tạo FastAPI app instance - core của toàn bộ backend
app = FastAPI(
    title=settings.API_TITLE,  # Title hiển thị trong Swagger docs (từ config.py)
    description="API cho hệ thống quản lý nông nghiệp - Kết nối PostgreSQL",  # Mô tả API
    version=settings.API_VERSION,  # Version của API (từ config.py)
    docs_url="/docs",    # URL để xem Swagger UI: http://localhost:8000/docs
    redoc_url="/redoc"   # URL để xem ReDoc UI: http://localhost:8000/redoc
)

# ========== CONFIGURE CORS MIDDLEWARE ==========
# CORS (Cross-Origin Resource Sharing) cho phép Frontend (port 5173) gọi API từ Backend (port 8000)
# Nếu không có CORS, browser sẽ block requests từ origin khác
app.add_middleware(
    CORSMiddleware,                      # Middleware class của FastAPI
    allow_origins=settings.cors_origins_list,  # Danh sách origins được phép: ["http://localhost:5173", "*"]
    allow_credentials=True,              # Cho phép gửi cookies/credentials
    allow_methods=["*"],                 # Cho phép tất cả HTTP methods: GET, POST, PUT, DELETE, PATCH
    allow_headers=["*"],                 # Cho phép tất cả headers: Content-Type, Authorization, etc.
)


# ========== STARTUP & SHUTDOWN EVENTS ==========

@app.on_event("startup")
async def startup_event():
    """
    Event handler chạy khi FastAPI app khởi động
    
    Cách hoạt động:
    1. Log thông tin server (URL, docs URL)
    2. Test kết nối database bằng test_connection()
    3. Lấy thông tin schema và số lượng bảng
    4. Log kết quả connection
    
    Kết nối đến:
    - database.py: test_connection(), get_table_count()
    - Tự động được FastAPI gọi khi server start
    """
    logger.info("🚀 Starting FastAPI Backend Server...")
    logger.info(f"📡 API running at: http://localhost:8000")
    logger.info(f"📚 API Docs at: http://localhost:8000/docs")
    
    # Test database connection khi server khởi động
    if test_connection():  # Return True nếu connect thành công
        table_info = get_table_count()  # Lấy thông tin schema và tables
        logger.info(f"✅ Connected to schema: {table_info.get('schema')}")  # Log schema name: "nongsan"
        logger.info(f"✅ Total tables: {table_info.get('count')}")           # Log số bảng: 18
    else:
        logger.error("❌ Database connection failed!")  # Log error nếu không connect được


@app.on_event("shutdown")
async def shutdown_event():
    """
    Event handler chạy khi FastAPI app shutdown
    
    Cách hoạt động:
    1. Log message khi server tắt
    2. Có thể thêm cleanup code ở đây (close connections, save state, etc.)
    
    Kết nối đến:
    - Tự động được FastAPI gọi khi server stop (Ctrl+C hoặc kill process)
    """
    logger.info("👋 Shutting down FastAPI Backend Server...")


# ========== INCLUDE ROUTERS ==========
# Register các route modules vào FastAPI app
# Mỗi router có 1 prefix (ví dụ: /api) để tổ chức endpoints

# Include farms router
# Endpoints: /api/farms/, /api/farms/{id}, /api/farms/code/{code}
# Handles: GET, POST, PUT, DELETE operations cho Vùng trồng
app.include_router(farms.router, prefix=settings.API_PREFIX)  # settings.API_PREFIX = "/api"

# Include charts router
# Endpoints: /api/dashboard/stats, /api/charts/export-markets, /api/charts/crop-production, etc.
# Handles: Lấy dữ liệu thống kê cho biểu đồ
app.include_router(charts.router, prefix=settings.API_PREFIX)

# Include diary router
# Endpoints: /api/diary/, /api/diary/{id}, /api/diary/farm/{vung_id}
# Handles: CRUD operations cho Nhật ký hoạt động
app.include_router(diary.router, prefix=settings.API_PREFIX)


# ========== ROOT & HEALTH ENDPOINTS ==========

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🌾 Agriculture Management API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "health": "/api/health"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    db_connected = test_connection()
    table_info = get_table_count()
    
    return {
        "status": "healthy" if db_connected else "unhealthy",
        "message": "Backend API is running",
        "version": settings.API_VERSION,
        "database_connected": db_connected,
        "total_tables": table_info.get('count', 0),
        "schema": table_info.get('schema', 'unknown')
    }


# ========== RUN APPLICATION ==========

if __name__ == '__main__':
    print("🚀 Starting FastAPI Backend Server...")
    print(f"📡 API running at: http://localhost:8000")
    print(f"📚 API Docs at: http://localhost:8000/docs")
    print(f"🔗 Database: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    print(f"📊 Schema: {settings.DB_SCHEMA}")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

