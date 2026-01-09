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
from routes import fertilizers  # Fertilizers APIs: Quản lý danh mục phân bón
from routes import pesticides   # Pesticides APIs: Quản lý danh mục thuốc BVTV
from routes import qr       # QR APIs: Tạo QR code và traceability
from routes import enhanced # Enhanced APIs: Facilities với coordinates và views mới

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

# Include fertilizers router
# Endpoints: /api/fertilizers/, /api/fertilizers/categories/
# Handles: Quản lý danh mục phân bón
app.include_router(fertilizers.router, prefix=settings.API_PREFIX)

# Include pesticides router
# Endpoints: /api/pesticides/, /api/pesticides/groups/
# Handles: Quản lý danh mục thuốc BVTV
app.include_router(pesticides.router, prefix=settings.API_PREFIX)

# Include QR router
# Endpoints: /api/qr/generate/{ma_vung}, /api/qr/trace/{ma_vung}
# Handles: Tạo QR code và traceability công khai
app.include_router(qr.router, prefix=settings.API_PREFIX)

# Include enhanced router
# Endpoints: /api/enhanced/facilities, /api/enhanced/facilities/map, /api/enhanced/farms/crops, etc.
# Handles: Enhanced queries với coordinates, views và statistics
app.include_router(enhanced.router, prefix=settings.API_PREFIX)


# ========== ROOT & HEALTH ENDPOINTS ==========

@app.get("/")
async def root():
    """
    Root endpoint - Trang chủ của API
    
    Endpoint: GET /
    Method: GET
    Authentication: None (public)
    
    Response:
    {
        "message": "🌾 Agriculture Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }
    
    Usage:
    - Kiểm tra xem API có đang chạy không
    - Xem version hiện tại
    - Link đến docs và health check
    
    Kết nối đến:
    - config.py: settings.API_VERSION
    - Browser: http://localhost:8000/ sẽ trả về JSON này
    """
    return {
        "message": "🌾 Agriculture Management API",  # Welcome message
        "version": settings.API_VERSION,            # Version từ config (1.0.0)
        "docs": "/docs",                             # Link đến Swagger UI
        "health": "/api/health"                      # Link đến health check endpoint
    }


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint - Kiểm tra trạng thái API và Database
    
    Endpoint: GET /api/health
    Method: GET
    Authentication: None (public)
    
    Cách hoạt động:
    1. Test kết nối database bằng test_connection()
    2. Lấy thông tin tables từ get_table_count()
    3. Return status "healthy" hoặc "unhealthy" tùy DB connection
    
    Response:
    {
        "status": "healthy",              // "healthy" or "unhealthy"
        "message": "Backend API is running",
        "version": "1.0.0",
        "database_connected": true,       // true/false
        "total_tables": 18,               // Số bảng trong schema
        "schema": "nongsan"               // Schema name
    }
    
    Usage:
    - Frontend gọi để check backend có sẵn sàng không
    - Monitoring tools check health status
    - Debugging database connection issues
    
    Kết nối đến:
    - database.py: test_connection(), get_table_count()
    - config.py: settings.API_VERSION
    - Frontend: src/services/api.js -> getHealthStatus()
    """
    db_connected = test_connection()      # Test DB connection (return bool)
    table_info = get_table_count()        # Get schema info (return dict)
    
    return {
        "status": "healthy" if db_connected else "unhealthy",  # Trạng thái tổng thể
        "message": "Backend API is running",                    # Message
        "version": settings.API_VERSION,                        # API version
        "database_connected": db_connected,                     # DB connection status
        "total_tables": table_info.get('count', 0),            # Số bảng (default 0 nếu lỗi)
        "schema": table_info.get('schema', 'unknown')          # Schema name (default "unknown" nếu lỗi)
    }


# ========== RUN APPLICATION ==========
# Code này chỉ chạy khi execute file trực tiếp: python app.py
# Không chạy khi import: from app import app

if __name__ == '__main__':
    # Print startup information ra console
    print("🚀 Starting FastAPI Backend Server...")
    print(f"📡 API running at: http://localhost:8000")
    print(f"📚 API Docs at: http://localhost:8000/docs")
    print(f"🔗 Database: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")  # DB connection string
    print(f"📊 Schema: {settings.DB_SCHEMA}")  # Schema name: "nongsan"
    
    # Start Uvicorn ASGI server
    uvicorn.run(
        "app:app",          # Module:instance (app.py:app)
        host="0.0.0.0",     # Listen on all network interfaces (0.0.0.0 = public, không chỉ localhost)
        port=8000,          # Port 8000 (http://localhost:8000)
        reload=True,        # Auto-reload khi code thay đổi (chỉ dùng trong development)
        log_level="info"    # Log level: info (log mọi request và response)
    )
