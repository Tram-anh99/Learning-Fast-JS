# 🚀 FastAPI Backend - API Integration Guide

## ✅ Hoàn Thành

Backend FastAPI đã được thiết lập hoàn chỉnh với:

-    ✅ Kết nối PostgreSQL (port 5433, schema `nongsan`)
-    ✅ SQLAlchemy ORM với 12 models
-    ✅ Pydantic schemas cho validation
-    ✅ 3 nhóm API routes: Farms, Charts, Diary
-    ✅ CORS middleware cho frontend
-    ✅ Auto-reload development mode
-    ✅ Interactive API docs (Swagger UI)

## 🔗 Kết Nối Database

### Thông Tin Kết Nối

```
Host: localhost
Port: 5433
Database: postgres
Schema: nongsan
User: postgres
Password: 123456 (hoặc 000000)
```

### Test Kết Nối

```bash
cd Backend
./test_db.sh
```

## 🚀 Khởi Động Server

### Tự Động (Khuyến nghị)

```bash
cd Backend
./start.sh
```

### Thủ Công

```bash
cd Backend
source .venv/bin/activate
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Server sẽ chạy tại:

-    **API Base:** http://localhost:8000
-    **Swagger Docs:** http://localhost:8000/docs
-    **ReDoc:** http://localhost:8000/redoc

## 📊 API Endpoints Overview

### 1. Health & Info

```bash
GET /                    # Root info
GET /api/health          # Health check with DB status
```

### 2. Farms (Vùng Trồng - MSVT)

```bash
# List & Search
GET /api/farms?skip=0&limit=100&search=query&trang_thai_id=1

# Details
GET /api/farms/{id}
GET /api/farms/by-code/{ma_vung}

# CRUD
POST   /api/farms       # Create (requires VungTrongCreate schema)
PUT    /api/farms/{id}  # Update
DELETE /api/farms/{id}  # Delete
```

**Request Example (Create Farm):**

```json
{
     "ma_vung": "MSVT2024001",
     "ten_vung": "Vườn Xoài Cát Chu",
     "dia_chi": "Xã Tân Thạnh, Huyện Châu Thành",
     "dien_tich_ha": 5.2,
     "ngay_cap_ma": "2024-01-15",
     "ngay_het_han": "2025-01-15",
     "chu_vung_id": 1,
     "trang_thai_id": 1,
     "toa_do": [
          { "latitude": 10.123, "longitude": 106.456, "thu_tu": 1 },
          { "latitude": 10.124, "longitude": 106.457, "thu_tu": 2 }
     ]
}
```

### 3. Charts & Statistics

```bash
GET /api/charts/dashboard-stats      # Overview stats
GET /api/charts/export-markets       # Pie chart data
GET /api/charts/crop-production      # Bar chart data
GET /api/charts/productivity-trend   # Line chart data (query: years=5)
GET /api/charts/farm-status          # Status distribution
GET /api/charts/activity-timeline    # Timeline (query: days=30)
```

**Response Example (Dashboard Stats):**

```json
{
     "total_farms": 150,
     "active_farms": 142,
     "total_area_ha": 1250.75,
     "total_production": 5420.3,
     "recent_activities": 87,
     "chart_data": {}
}
```

### 4. Diary (Nhật Ký Canh Tác)

```bash
# List with filters
GET /api/diary?vung_trong_id=1&from_date=2024-01-01&to_date=2024-12-31

# CRUD
GET    /api/diary/{id}
POST   /api/diary
PUT    /api/diary/{id}
DELETE /api/diary/{id}

# Lookup
GET /api/diary/activity-types  # List all activity types
```

**Request Example (Create Diary):**

```json
{
     "vung_trong_id": 1,
     "loai_hoat_dong_id": 2,
     "ngay_thuc_hien": "2024-12-31",
     "mo_ta": "Bón phân NPK cho xoài",
     "phan_bon_id": 5,
     "luong_su_dung": 50.0,
     "don_vi": "kg",
     "nguoi_thuc_hien": "Nguyễn Văn A"
}
```

## 🎨 Frontend Integration

### Vue 3 + Fetch API

```javascript
// Base API URL
const API_BASE = "http://localhost:8000/api";

// Fetch farms
async function getFarms(limit = 100) {
     const response = await fetch(`${API_BASE}/farms?limit=${limit}`);
     const data = await response.json();
     return data;
}

// Create farm
async function createFarm(farmData) {
     const response = await fetch(`${API_BASE}/farms`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(farmData),
     });
     return await response.json();
}

// Get chart data
async function getMarketChart() {
     const response = await fetch(`${API_BASE}/charts/export-markets`);
     return await response.json();
}
```

### Vue 3 + Axios

```javascript
import axios from "axios";

const api = axios.create({
     baseURL: "http://localhost:8000/api",
     headers: { "Content-Type": "application/json" },
});

// Get farms
const getFarms = async () => {
     const { data } = await api.get("/farms");
     return data;
};

// Create diary entry
const createDiary = async (entry) => {
     const { data } = await api.post("/diary", entry);
     return data;
};
```

## 📦 Data Models

### Main Models (SQLAlchemy ORM)

1. **VungTrong** - Farm zones with MSVT codes
2. **ToaDoVung** - Polygon coordinates
3. **LoaiCay** - Crop types
4. **VungCayTrong** - Farm-Crop junction (N-N)
5. **ThiTruong** - Export markets
6. **CayThiTruong** - Crop-Market junction (N-N)
7. **ChuVung** - Farm owners
8. **TrangThai** - Status tracking
9. **LichSuCanhTac** - Farming diary
10. **LoaiHoatDong** - Activity types
11. **ThongKeHeThong** - System statistics
12. **ChungNhan** - Certifications
13. **DiemSauBenh** - Pest/disease tracking

### Pydantic Schemas (Request/Response)

See [schemas.py](schemas.py) for full definitions:

-    `VungTrongCreate`, `VungTrongResponse`, `VungTrongDetail`
-    `LichSuCanhTacCreate`, `LichSuCanhTacResponse`
-    `ChartData`, `DashboardStats`
-    `PaginatedResponse`, `ResponseBase`

## 🔧 Development Tips

### Database Migrations (Alembic)

```bash
# Initialize (first time only)
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Add new table"

# Apply migration
alembic upgrade head
```

### Adding New Endpoints

1. Create model in `models/` directory
2. Add schema in `schemas.py`
3. Create router in `routes/` directory
4. Include router in `app.py`

Example:

```python
# routes/new_feature.py
from fastapi import APIRouter
router = APIRouter(prefix="/new-feature", tags=["NewFeature"])

@router.get("/")
async def get_items():
    return {"items": []}

# app.py
from routes import new_feature
app.include_router(new_feature.router, prefix=settings.API_PREFIX)
```

### Testing APIs

```bash
# Interactive Swagger UI
open http://localhost:8000/docs

# curl
curl http://localhost:8000/api/health

# httpie (install: brew install httpie)
http GET http://localhost:8000/api/farms limit==10

# Python
python3 -c "import requests; print(requests.get('http://localhost:8000/api/health').json())"
```

## 📚 Project Structure

```
Backend/
├── app.py                 # Main FastAPI app
├── config.py              # Settings & environment
├── database.py            # DB connection & session
├── schemas.py             # Pydantic models
│
├── models/                # SQLAlchemy ORM
│   ├── vung_trong.py
│   ├── loai_cay.py
│   ├── thi_truong.py
│   ├── chu_vung.py
│   ├── trang_thai.py
│   ├── lich_su.py
│   ├── thong_ke.py
│   ├── chung_nhan.py
│   └── sau_benh.py
│
├── routes/                # API endpoints
│   ├── farms.py          # Farm management
│   ├── charts.py         # Charts & stats
│   └── diary.py          # Diary entries
│
├── .env                   # Environment variables
├── requirements-minimal.txt
├── setup.sh              # Setup script
├── test_db.sh            # DB test script
└── start.sh              # Start server script
```

## ⚠️ Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
brew services list | grep postgres

# Test connection
./test_db.sh

# Try alternative password
# Edit .env: DB_PASSWORD=000000
```

### Port Already in Use

```bash
# Find and kill process
lsof -ti :8000 | xargs kill -9

# Or use different port
uvicorn app:app --port 8001
```

### Module Import Error

```bash
# Check you're in virtual environment
which python  # Should show .venv/bin/python

# Reinstall dependencies
pip install -r requirements-minimal.txt
```

## 🔐 Security Checklist

-    [ ] Change `SECRET_KEY` in production
-    [ ] Use strong database password
-    [ ] Limit CORS origins to specific domains
-    [ ] Add API authentication (JWT)
-    [ ] Enable HTTPS in production
-    [ ] Rate limiting for public endpoints
-    [ ] SQL injection protection (✅ SQLAlchemy ORM)
-    [ ] Input validation (✅ Pydantic)

## 📞 Next Steps

1. ✅ Backend API đã sẵn sàng
2. 🔄 Kết nối Frontend với API endpoints
3. 📝 Thêm dữ liệu test vào database
4. 🎨 Cập nhật frontend components để gọi API
5. 🧪 Test integration giữa frontend-backend

## 🔗 Links

-    **API Docs:** http://localhost:8000/docs
-    **ReDoc:** http://localhost:8000/redoc
-    **Database Schema:** `/Database/README.md`
-    **Frontend:** `/Frontend/README.md`

---

**✨ Backend FastAPI + PostgreSQL Integration Complete!**
