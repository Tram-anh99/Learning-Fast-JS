"""
========== TEST BACKEND - Quick Health Check ==========
File: test_backend.py
Mục đích: Test nhanh Backend API mà không cần models phức tạp
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Tạo FastAPI app đơn giản
app = FastAPI(title="Test Backend API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend is running!"}

@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "message": "Test backend OK",
        "version": "test"
    }

@app.get("/api/farms/")
def get_farms():
    # Mock data đơn giản
    return {
        "total": 3,
        "data": [
            {"id": 1, "ma_vung": "MSVT001", "ten_vung": "Vườn A"},
            {"id": 2, "ma_vung": "MSVT002", "ten_vung": "Vườn B"},
            {"id": 3, "ma_vung": "MSVT003", "ten_vung": "Vườn C"}
        ]
    }

if __name__ == "__main__":
    print("🚀 Starting Test Backend on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
