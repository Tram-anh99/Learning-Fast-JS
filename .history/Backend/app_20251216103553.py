"""
========== FastAPI Backend Application ==========
Purpose: API server cho ứng dụng nông nghiệp
Author: Learning-Fast-JS
Date: 2025-12-16
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Agriculture Management API",
    description="API cho hệ thống quản lý nông nghiệp",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== PYDANTIC MODELS ==========

class HealthResponse(BaseModel):
    status: str
    message: str
    version: str


class DiaryEntry(BaseModel):
    id: Optional[int] = None
    type: str
    title: str
    field: str
    details: str
    dateDay: str
    dateMonth: str


class DiaryResponse(BaseModel):
    success: bool
    message: str
    data: Optional[DiaryEntry] = None


# ========== API ROUTES ==========

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Backend API is running",
        "version": "1.0.0"
    }


@app.get("/api/charts/export-markets")
async def get_export_markets():
    """
    Lấy dữ liệu thị trường xuất khẩu
    Returns: JSON data for export market chart
    """
    return {
        "labels": ["Trung Quốc", "Hoa Kỳ", "Nhật Bản", "Hàn Quốc", "EU"],
        "datasets": [{
            "data": [35, 25, 18, 12, 10],
            "backgroundColor": [
                "#FF6384",
                "#36A2EB", 
                "#FFCE56",
                "#4BC0C0",
                "#9966FF"
            ]
        }]
    }


@app.get("/api/charts/crop-production")
async def get_crop_production():
    """
    Lấy dữ liệu sản lượng cây trồng
    Returns: JSON data for crop production chart
    """
    return {
        "labels": ["Xoài", "Thanh Long", "Nhãn", "Vải", "Chôm Chôm"],
        "datasets": [{
            "label": "Sản lượng (tấn)",
            "data": [450, 380, 320, 280, 150],
            "backgroundColor": "#10b981"
        }]
    }


@app.get("/api/charts/productivity-trend")
async def get_productivity_trend():
    """
    Lấy dữ liệu xu hướng năng suất
    Returns: JSON data for productivity trend chart
    """
    return {
        "labels": ["2020", "2021", "2022", "2023", "2024"],
        "datasets": [{
            "label": "Năng suất (tạ/ha)",
            "data": [38.5, 41.2, 43.8, 45.5, 47.2],
            "borderColor": "#3b82f6",
            "tension": 0.4
        }]
    }


@app.get("/api/farms")
async def get_farms():
    """
    Lấy danh sách vùng trồng
    Returns: List of farm areas
    """
    # TODO: Kết nối database và query dữ liệu thực
    return []


@app.get("/api/diary", response_model=List[DiaryEntry])
async def get_diary_entries():
    """
    Lấy danh sách nhật ký
    """
    # TODO: Lấy từ database
    return []


@app.post("/api/diary", response_model=DiaryResponse, status_code=201)
async def create_diary_entry(entry: DiaryEntry):
    """
    Tạo nhật ký mới
    """
    # TODO: Lưu vào database
    return {
        "success": True,
        "message": "Đã lưu nhật ký thành công",
        "data": entry
    }


# ========== RUN APPLICATION ==========

if __name__ == '__main__':
    print("🚀 Starting FastAPI Backend Server...")
    print("📡 API running at: http://localhost:8000")
    print("📚 API Docs at: http://localhost:8000/docs")
    print("🔗 Frontend should connect to: http://localhost:8000/api/...")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
