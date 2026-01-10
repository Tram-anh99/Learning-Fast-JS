# System Architecture Documentation

## Hệ Thống Quản Lý Nông Nghiệp & Truy Xuất Nguồn Gốc

**Version:** 2.0  
**Last Updated:** January 10, 2026  
**Tech Stack:** Vue.js 3 + FastAPI + PostgreSQL

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Technology Stack](#technology-stack)
4. [Component Details](#component-details)
5. [Data Flow](#data-flow)
6. [Security](#security)
7. [Deployment](#deployment)
8. [Scalability](#scalability)

---

## 🎯 System Overview

### Purpose
Hệ thống quản lý nông nghiệp hiện đại với khả năng truy xuất nguồn gốc nông sản thông qua QR code, tích hợp bản đồ GIS, và quản lý toàn diện quy trình canh tác.

### Key Objectives
- ✅ **Transparency:** Minh bạch nguồn gốc nông sản
- ✅ **Traceability:** Truy xuất được toàn bộ lịch sử canh tác
- ✅ **Management:** Quản lý hiệu quả vùng trồng, cơ sở sản xuất
- ✅ **Compliance:** Đáp ứng tiêu chuẩn VietGAP, GlobalGAP, Organic
- ✅ **Accessibility:** Dễ sử dụng cho cả nông dân và quản lý

### Target Users
1. **Nông dân:** Quản lý vùng trồng, nhật ký canh tác
2. **Quản lý:** Giám sát, thống kê, báo cáo
3. **Người tiêu dùng:** Quét QR để xem nguồn gốc sản phẩm
4. **Cơ quan nhà nước:** Giám sát, cấp chứng nhận

---

## 🏗️ Architecture Diagram

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Web App    │  │  Mobile QR   │  │   Admin      │          │
│  │  (Vue.js 3)  │  │   Scanner    │  │  Dashboard   │          │
│  │              │  │              │  │              │          │
│  │ - Bản đồ     │  │ - Quét QR    │  │ - Thống kê   │          │
│  │ - Quản lý    │  │ - Truy xuất  │  │ - Báo cáo    │          │
│  │ - Nhật ký    │  │ - Công khai  │  │ - Quản trị   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                   │                  │                 │
│         └───────────────────┴──────────────────┘                 │
│                             │                                     │
│                             ▼                                     │
│                    ┌────────────────┐                            │
│                    │  NGINX/CDN     │                            │
│                    │  (Port 80/443) │                            │
│                    └────────────────┘                            │
│                             │                                     │
└─────────────────────────────┼─────────────────────────────────────┘
                              │
┌─────────────────────────────┼─────────────────────────────────────┐
│                         API GATEWAY                              │
├─────────────────────────────┼─────────────────────────────────────┤
│                             ▼                                     │
│                    ┌────────────────┐                            │
│                    │   FastAPI      │                            │
│                    │  (Port 8000)   │                            │
│                    │                │                            │
│                    │ - REST API     │                            │
│                    │ - CORS         │                            │
│                    │ - Validation   │                            │
│                    │ - Auth (JWT)   │                            │
│                    └────────────────┘                            │
│                             │                                     │
│         ┌───────────────────┼───────────────────┐                │
│         │                   │                   │                │
│         ▼                   ▼                   ▼                │
│  ┌──────────┐       ┌──────────┐       ┌──────────┐            │
│  │  Farms   │       │  Charts  │       │  Diary   │            │
│  │  Routes  │       │  Routes  │       │  Routes  │            │
│  └──────────┘       └──────────┘       └──────────┘            │
│         │                   │                   │                │
│  ┌──────────┐       ┌──────────┐       ┌──────────┐            │
│  │   QR     │       │ GeoJSON  │       │ Enhanced │            │
│  │  Routes  │       │  Routes  │       │  Routes  │            │
│  └──────────┘       └──────────┘       └──────────┘            │
│                                                                   │
└─────────────────────────────┬─────────────────────────────────────┘
                              │
┌─────────────────────────────┼─────────────────────────────────────┐
│                       DATA LAYER                                  │
├─────────────────────────────┼─────────────────────────────────────┤
│                             ▼                                     │
│                    ┌────────────────┐                            │
│                    │  PostgreSQL 16 │                            │
│                    │  (Port 5432)   │                            │
│                    │                │                            │
│                    │ Schema: nongsan│                            │
│                    │ Tables: 31     │                            │
│                    │ Views: 5       │                            │
│                    │                │                            │
│                    │ - Farms        │                            │
│                    │ - Activities   │                            │
│                    │ - Facilities   │                            │
│                    │ - Products     │                            │
│                    │ - Locations    │                            │
│                    └────────────────┘                            │
│                             │                                     │
│                    ┌────────┴────────┐                           │
│                    │                 │                           │
│                    ▼                 ▼                           │
│            ┌──────────┐      ┌──────────┐                       │
│            │  Backup  │      │   Logs   │                       │
│            │  (Daily) │      │ (Audit)  │                       │
│            └──────────┘      └──────────┘                       │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Map Tiles  │  │   QR Code    │  │   Email      │          │
│  │  (OpenStreet)│  │  Generator   │  │  Service     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### Layered Architecture

```
┌───────────────────────────────────────────────────┐
│         PRESENTATION LAYER (Frontend)             │
│  Vue.js 3 + Vite + Tailwind CSS + Leaflet.js    │
│  - Components (Reusable UI)                       │
│  - Views (Page-level components)                  │
│  - Router (Navigation)                            │
│  - Composables (Business logic)                   │
└───────────────────────────────────────────────────┘
                       │
                       ▼ HTTP/HTTPS
┌───────────────────────────────────────────────────┐
│          APPLICATION LAYER (Backend)              │
│  FastAPI + Uvicorn + Pydantic                     │
│  - Routes (API endpoints)                         │
│  - Models (Data validation)                       │
│  - Services (Business logic)                      │
│  - Middleware (Auth, CORS, Logging)               │
└───────────────────────────────────────────────────┘
                       │
                       ▼ psycopg2
┌───────────────────────────────────────────────────┐
│           DATA ACCESS LAYER                       │
│  PostgreSQL 16 + PostGIS (optional)               │
│  - Tables (Data storage)                          │
│  - Views (Aggregated data)                        │
│  - Indexes (Performance)                          │
│  - Constraints (Data integrity)                   │
└───────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Frontend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | Vue.js | 3.5.13 | Progressive JavaScript framework |
| **Build Tool** | Vite | 6.0.5 | Fast dev server & build tool |
| **Routing** | Vue Router | 4.5.0 | Client-side routing |
| **HTTP Client** | Axios | 1.7.9 | API requests |
| **UI Framework** | Tailwind CSS | 3.4.17 | Utility-first CSS |
| **Charts** | Chart.js | 4.4.7 | Data visualization |
| **Maps** | Leaflet.js | 1.9.4 | Interactive maps |
| **QR Code** | qrcode.vue | 3.5.0 | QR generation |

**Frontend Structure:**
```
Frontend/
├── src/
│   ├── App.vue              # Root component
│   ├── main.js              # Entry point
│   ├── assets/              # Static assets (CSS, images)
│   ├── components/          # Reusable components (20+)
│   │   ├── BarChartComponent.vue
│   │   ├── MapComponent.vue
│   │   ├── DiaryActivityForm.vue
│   │   └── ...
│   ├── composables/         # Business logic hooks (6)
│   │   ├── useDiary.js
│   │   ├── useMapLogic.js
│   │   └── ...
│   ├── router/              # Route definitions
│   │   └── index.js
│   └── views/               # Page components (5)
│       ├── HomeView.vue     # Bản đồ
│       ├── QuanLyView.vue   # Quản lý
│       ├── DiaryPage.vue    # Nhật ký
│       └── TraceabilityPage.vue # Truy xuất
├── public/                  # Public assets
├── index.html               # HTML template
├── vite.config.js           # Vite configuration
├── tailwind.config.js       # Tailwind configuration
└── package.json             # Dependencies
```

### Backend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | FastAPI | 0.128.0 | Modern Python web framework |
| **Server** | Uvicorn | 0.34.0 | ASGI server |
| **ORM** | SQLAlchemy | 2.0.39 | SQL toolkit & ORM |
| **Database Driver** | psycopg2-binary | 2.9.10 | PostgreSQL adapter |
| **Validation** | Pydantic | 2.10.6 | Data validation |
| **Migration** | Alembic | 1.17.0 | Database migrations |
| **Data Processing** | Pandas | 2.3.2 | Data manipulation |
| **QR Code** | qrcode | 8.0 | QR generation |

**Backend Structure:**
```
Backend/
├── app.py                   # Main application
├── config.py                # Configuration (DB, API)
├── database.py              # DB connection utilities
├── routes/                  # API route modules (8)
│   ├── farms.py             # Farm CRUD APIs
│   ├── charts.py            # Statistics APIs
│   ├── diary.py             # Activity log APIs
│   ├── qr.py                # QR & traceability
│   ├── geojson.py           # GeoJSON map data
│   ├── enhanced.py          # Enhanced queries
│   ├── fertilizers.py       # Fertilizer catalog
│   └── pesticides.py        # Pesticide catalog
├── models/                  # Pydantic models (if separated)
├── requirements.txt         # Python dependencies (full)
├── requirements-minimal.txt # Minimal dependencies
└── .env                     # Environment variables
```

### Database

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **RDBMS** | PostgreSQL | 16.x | Primary database |
| **Schema** | nongsan | - | Main schema |
| **Extension** | PostGIS | (optional) | Geographic data |
| **Backup** | pg_dump | 16.x | Database backup |

**Database Configuration:**
```python
# config.py
DATABASE_URL = "postgresql://username:password@localhost:5432/nongsan_db"
SCHEMA = "nongsan"
```

---

## 🔧 Component Details

### 1. Frontend Components

#### Core Components

**`App.vue`** - Root component
- Manages global state
- Navigation sidebar
- Route transitions

**`HomeView.vue`** - Map view (Bản đồ)
- Interactive map với Leaflet.js
- Display farms, facilities
- Filter by location, crop type
- GeoJSON polygon/line rendering

**`QuanLyView.vue`** - Management view (Quản lý)
- Dashboard with statistics
- Charts (Bar, Line, Pie)
- Data tables with pagination
- Export functionality

**`DiaryPage.vue`** - Activity log (Nhật ký canh tác)
- Activity form (Add/Edit)
- Activity history timeline
- Activity selector dropdown
- Filter by date, farm, activity type

**`TraceabilityPage.vue`** - Public traceability (Truy xuất)
- QR scanner
- Display farm info
- Show activity history
- Show certifications

#### Reusable Components (20+)

**Charts:**
- `BarChartComponent.vue` - Bar charts
- `LineChartComponent.vue` - Line charts
- `PieChartComponent.vue` - Pie charts
- `ProductivityLineChart.vue` - Custom productivity chart
- `StatsBarComponent.vue` - Statistics bar

**Map:**
- `MapComponent.vue` - Leaflet map wrapper
- `MapLayerControl.vue` - Layer toggle
- `MapLayerSelector.vue` - Layer selector dropdown

**Diary:**
- `DiaryActivityForm.vue` - Activity input form
- `DiaryActivityHistory.vue` - Activity timeline
- `DiaryActivitySelector.vue` - Activity type dropdown

**Data Display:**
- `DataTableComponent.vue` - Generic data table
- `FilterTabs.vue` - Tab filters
- `HomeDetailView.vue` - Farm detail view
- `HomeListItem.vue` - Farm list item
- `ProductList.vue` - Product list
- `CropDetailsComponent.vue` - Crop details

**QR:**
- `QRModal.vue` - QR display modal
- `QRScanner.vue` - QR scanner component

**Other:**
- `SidebarHeader.vue` - Sidebar header component

#### Composables (Business Logic)

```javascript
// composables/useDiary.js
export function useDiary() {
    const activities = ref([]);
    const loadActivities = async (vungId) => { /*...*/ };
    const addActivity = async (data) => { /*...*/ };
    return { activities, loadActivities, addActivity };
}

// composables/useMapLogic.js
export function useMapLogic() {
    const map = ref(null);
    const initMap = (container) => { /*...*/ };
    const addMarkers = (farms) => { /*...*/ };
    return { map, initMap, addMarkers };
}

// composables/useCharts.js
export function useCharts() {
    const chartData = ref(null);
    const loadChartData = async () => { /*...*/ };
    return { chartData, loadChartData };
}

// composables/useCropData.js
export function useCropData() {
    const crops = ref([]);
    const loadCrops = async () => { /*...*/ };
    return { crops, loadCrops };
}

// composables/useHome.js
export function useHome() {
    const farms = ref([]);
    const selectedFarm = ref(null);
    return { farms, selectedFarm };
}

// composables/useLineChartData.js
export function useLineChartData() {
    const lineData = ref(null);
    const loadLineData = async () => { /*...*/ };
    return { lineData, loadLineData };
}
```

### 2. Backend Routes

#### API Endpoints Summary

| Route Module | Base Path | Endpoints | Purpose |
|-------------|-----------|-----------|---------|
| **farms** | `/api/farms` | 6 | Farm CRUD operations |
| **charts** | `/api` | 8 | Statistics & charts data |
| **diary** | `/api/diary` | 5 | Activity log management |
| **qr** | `/api/qr` | 3 | QR generation & traceability |
| **geojson** | `/api/geojson` | 6 | GeoJSON map data |
| **enhanced** | `/api/enhanced` | 6 | Enhanced queries with coordinates |
| **fertilizers** | `/api/fertilizers` | 3 | Fertilizer catalog |
| **pesticides** | `/api/pesticides` | 3 | Pesticide catalog |

**Total:** ~40 endpoints

#### Detailed Route Specifications

**farms.py:**
```python
GET    /api/farms/                    # List all farms
POST   /api/farms/                    # Create farm
GET    /api/farms/{id}                # Get farm by ID
PUT    /api/farms/{id}                # Update farm
DELETE /api/farms/{id}                # Delete farm
GET    /api/farms/code/{ma_vung}     # Get farm by code
```

**charts.py:**
```python
GET /api/dashboard/stats              # Dashboard statistics
GET /api/charts/export-markets        # Export market chart
GET /api/charts/crop-production       # Crop production chart
GET /api/charts/facilities-by-type    # Facilities by type
GET /api/charts/farm-status           # Farm status distribution
GET /api/charts/monthly-activities    # Monthly activities
GET /api/charts/crop-areas            # Crop area by province
GET /api/charts/productivity-trends   # Productivity trends
```

**diary.py:**
```python
GET    /api/diary/                    # List activities
POST   /api/diary/                    # Create activity
GET    /api/diary/{id}                # Get activity
PUT    /api/diary/{id}                # Update activity
DELETE /api/diary/{id}                # Delete activity
GET    /api/diary/farm/{vung_id}     # Get activities by farm
```

**geojson.py:** (NEW - Jan 10, 2026)
```python
GET /api/geojson/provinces            # Province polygons
GET /api/geojson/districts            # District polygons
GET /api/geojson/communes             # Commune polygons
GET /api/geojson/farms/boundaries     # Farm boundaries
GET /api/geojson/routes/lines         # Province connections
GET /api/geojson/info/{layer}/{id}    # Click info
```

---

## 🔄 Data Flow

### Request Flow

```
┌─────────┐
│  User   │
│ Browser │
└────┬────┘
     │ 1. HTTP Request (GET /api/farms)
     ▼
┌─────────────┐
│   Vite Dev  │
│   Server    │  (Development: localhost:5173)
│  (Port 5173)│
└─────┬───────┘
     │ 2. Proxy to Backend
     ▼
┌─────────────┐
│  FastAPI    │
│  Server     │  3. Route to handler
│ (Port 8000) │
└─────┬───────┘
     │ 4. Execute route function
     │    - Validate request
     │    - Call database
     ▼
┌─────────────┐
│ PostgreSQL  │
│  Database   │  5. Execute SQL query
│ (Port 5432) │
└─────┬───────┘
     │ 6. Return rows
     ▼
┌─────────────┐
│  FastAPI    │  7. Process data
│  Response   │     - Format JSON
│             │     - Add metadata
└─────┬───────┘
     │ 8. JSON Response
     ▼
┌─────────────┐
│  Vue.js     │  9. Update component
│  Component  │     - Render UI
│             │     - Show data
└─────────────┘
```

### Data Flow Examples

#### Example 1: Load Farms on Map

```javascript
// Frontend: HomeView.vue
onMounted(async () => {
    try {
        // 1. API call
        const response = await axios.get('http://localhost:8000/api/farms/');
        
        // 2. Store data
        farms.value = response.data;
        
        // 3. Render markers
        farms.value.forEach(farm => {
            addMarkerToMap(farm);
        });
    } catch (error) {
        console.error('Error loading farms:', error);
    }
});
```

```python
# Backend: routes/farms.py
@router.get("/farms/")
async def get_farms():
    # 1. Connect to database
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 2. Execute query
    cur.execute("""
        SELECT id, ma_vung, ten_vung, dien_tich, tinh_id
        FROM nongsan.vung_trong
        ORDER BY ngay_tao DESC
    """)
    
    # 3. Fetch results
    rows = cur.fetchall()
    
    # 4. Format response
    farms = [
        {
            "id": row[0],
            "ma_vung": row[1],
            "ten_vung": row[2],
            "dien_tich": float(row[3]) if row[3] else None,
            "tinh_id": row[4]
        }
        for row in rows
    ]
    
    # 5. Return JSON
    return {"data": farms, "count": len(farms)}
```

#### Example 2: QR Code Traceability

```
┌─────────┐
│Consumer │ Scans QR
└────┬────┘
     │ ma_vung = "VT000123"
     ▼
┌─────────────────────┐
│ TraceabilityPage.vue│
└─────────┬───────────┘
         │ GET /api/qr/trace/VT000123
         ▼
┌─────────────────────┐
│   qr.py Router      │
└─────────┬───────────┘
         │ Query farm + activities
         ▼
┌─────────────────────┐
│    PostgreSQL       │
│  - vung_trong       │
│  - lich_su_canh_tac │
│  - loai_cay         │
└─────────┬───────────┘
         │ Return JSON
         ▼
┌─────────────────────┐
│   Display:          │
│ - Farm name         │
│ - Location          │
│ - Crops             │
│ - Activity timeline │
│ - Certifications    │
└─────────────────────┘
```

---

## 🔒 Security

### Authentication & Authorization

**Current Status:** Basic (No authentication yet)

**Planned:**
```python
# JWT Authentication
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Verify JWT token
    # Return user object
    pass

@router.get("/farms/")
async def get_farms(current_user: User = Depends(get_current_user)):
    # Only authenticated users can access
    pass
```

### CORS Configuration

```python
# app.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE
    allow_headers=["*"],  # All headers
)
```

### Input Validation

```python
from pydantic import BaseModel, Field, validator

class FarmCreate(BaseModel):
    ma_vung: str = Field(..., min_length=3, max_length=50)
    ten_vung: str = Field(..., min_length=3, max_length=200)
    dien_tich: float = Field(gt=0, description="Area must be positive")
    
    @validator('ma_vung')
    def validate_ma_vung(cls, v):
        if not v.startswith('VT'):
            raise ValueError('ma_vung must start with VT')
        return v
```

### SQL Injection Prevention

```python
# ✅ SAFE: Parameterized query
cur.execute(
    "SELECT * FROM vung_trong WHERE ma_vung = %s",
    (ma_vung,)  # Automatically escaped
)

# ❌ UNSAFE: String concatenation
cur.execute(
    f"SELECT * FROM vung_trong WHERE ma_vung = '{ma_vung}'"
)
```

---

## 🚀 Deployment

### Development Environment

```bash
# Backend
cd Backend
python -m uvicorn app:app --reload --port 8000

# Frontend
cd Frontend
npm run dev  # Vite dev server on port 5173
```

### Production Deployment

#### Option 1: Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: nongsan_db
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  
  backend:
    build: ./Backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://admin:secure_password@postgres:5432/nongsan_db
    depends_on:
      - postgres
  
  frontend:
    build: ./Frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

#### Option 2: Traditional Server

```bash
# 1. Setup PostgreSQL
sudo apt install postgresql-16
sudo -u postgres createdb nongsan_db
sudo -u postgres psql -d nongsan_db -f backup.sql

# 2. Setup Backend
cd Backend
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000

# 3. Setup Frontend
cd Frontend
npm run build  # Build production assets
# Serve dist/ folder with Nginx
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name example.com;
    
    # Frontend
    location / {
        root /var/www/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📈 Scalability

### Performance Optimization

**Database:**
- ✅ Indexes on frequently queried columns
- ✅ Views for complex aggregations
- ⏳ Connection pooling (SQLAlchemy)
- ⏳ Read replicas for heavy read operations

**Backend:**
- ✅ Async endpoints (FastAPI)
- ⏳ Caching (Redis) for frequently accessed data
- ⏳ Background tasks (Celery) for heavy processing
- ⏳ API rate limiting

**Frontend:**
- ✅ Code splitting (Vite)
- ✅ Lazy loading components
- ⏳ CDN for static assets
- ⏳ Service worker for offline support

### Monitoring

**Planned:**
```python
# Add logging middleware
from fastapi import Request
import time

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    logger.info(f"{request.method} {request.url.path} - {duration:.3f}s")
    return response
```

---

## 📊 System Metrics

### Current System Statistics

**Database:**
- Tables: 31
- Records: ~45,000
- Size: ~50 MB
- Queries/sec: ~10 (dev environment)

**API:**
- Total Endpoints: ~40
- Avg Response Time: 50-100ms
- Request/sec: ~5 (dev environment)

**Frontend:**
- Components: 26
- Views: 5
- Bundle Size: ~2.5 MB (development)
- Load Time: <2s

---

## 🔄 CI/CD Pipeline (Planned)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          cd Backend
          pytest
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # SSH to server
          # Pull latest code
          # Restart services
```

---

**Document Owner:** Development Team  
**Last Review:** January 10, 2026  
**Next Review:** April 10, 2026
