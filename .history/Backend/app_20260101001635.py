"""
========== FastAPI Backend Application ==========
Purpose: API server cho ứng dụng nông nghiệp
Author: Learning-Fast-JS
Date: 2025-12-31 (Updated with PostgreSQL)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

# Import config and database
from config import settings
from database import test_connection, get_table_count

# Import routes
from routes import farms, charts, diary

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description="API cho hệ thống quản lý nông nghiệp - Kết nối PostgreSQL",
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== STARTUP & SHUTDOWN EVENTS ==========

@app.on_event("startup")
async def startup_event():
    """Kiểm tra kết nối database khi khởi động"""
    logger.info("🚀 Starting FastAPI Backend Server...")
    logger.info(f"📡 API running at: http://localhost:8000")
    logger.info(f"📚 API Docs at: http://localhost:8000/docs")
    
    # Test database connection
    if test_connection():
        table_info = get_table_count()
        logger.info(f"✅ Connected to schema: {table_info.get('schema')}")
        logger.info(f"✅ Total tables: {table_info.get('count')}")
    else:
        logger.error("❌ Database connection failed!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("👋 Shutting down FastAPI Backend Server...")


# ========== INCLUDE ROUTERS ==========

app.include_router(farms.router, prefix=settings.API_PREFIX)
app.include_router(charts.router, prefix=settings.API_PREFIX)
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

