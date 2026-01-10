# 📁 Project Structure Documentation

**Hệ Thống Quản Lý Nông Nghiệp & Truy Xuất Nguồn Gốc**

**Version:** 2.0  
**Last Updated:** January 10, 2026  
**Purpose:** Comprehensive guide to project file structure and organization

---

## 📋 Table of Contents

-    [Overview](#overview)
-    [Root Directory](#root-directory)
-    [Backend Structure](#backend-structure)
-    [Frontend Structure](#frontend-structure)
-    [Database Files](#database-files)
-    [Documentation](#documentation)
-    [File Naming Conventions](#file-naming-conventions)
-    [Import/Export Relationships](#importexport-relationships)
-    [Configuration Files](#configuration-files)

---

## 🎯 Overview

### Directory Statistics

```
Total Directories: 15+
Total Files: 100+
Lines of Code: ~15,000+
Documentation: 10+ files
```

### Technology Layers

```
┌─────────────────────────────────────┐
│         Frontend (Vue.js)           │  ← User Interface
├─────────────────────────────────────┤
│         Backend (FastAPI)           │  ← Business Logic
├─────────────────────────────────────┤
│       Database (PostgreSQL)         │  ← Data Storage
└─────────────────────────────────────┘
```

---

## 🏠 Root Directory

```
Learning-Fast-JS/
├── 📄 README.md                    # Project documentation (Main entry point)
├── 📄 start.sh                     # One-command startup script (500+ lines)
├── 📄 .gitignore                   # Git ignore patterns
│
├── 📄 CLEANUP_SUMMARY.txt          # Database cleanup summary
├── 📄 COMPONENT_ANALYSIS.md        # Component analysis report
├── 📄 FRONTEND_DOCUMENTATION.md    # Frontend docs
├── 📄 FUNCTIONAL_AUDIT_REPORT.md   # Functional audit
├── 📄 GITHUB_ISSUES.md             # GitHub issues tracking
├── 📄 REFACTORING_COMPLETE.md      # Refactoring notes
│
├── 📁 docs/                        # Documentation folder
├── 📁 Backend/                     # FastAPI backend
├── 📁 Frontend/                    # Vue.js frontend
├── 📁 Database/                    # Database scripts & backups
├── 📁 logs/                        # Application logs
└── 📁 wiki/                        # Project wiki
```

### 📄 Key Root Files

#### `README.md`

-    **Purpose:** Main project documentation
-    **Content:** Installation, usage, API docs, screenshots
-    **Audience:** Developers, users, thesis reviewers
-    **Lines:** 600+

#### `start.sh`

-    **Purpose:** Unified system startup script
-    **Content:**
     -    Prerequisites checking (Python, Node.js, PostgreSQL)
     -    Service management (start/stop/restart)
     -    Status monitoring
     -    Log viewing
     -    Database backup integration
-    **Commands:** `dev`, `stop`, `restart`, `status`, `logs`, `backup`, `help`
-    **Lines:** 500+
-    **Executable:** ✅ `chmod +x start.sh`

#### `.gitignore`

-    **Purpose:** Git version control exclusions
-    **Excludes:**
     -    `node_modules/`
     -    `venv/`, `__pycache__/`
     -    `.env`, `*.log`
     -    `backups/*.sql.gz`

---

## 🐍 Backend Structure

```
Backend/
├── 📄 app.py                       # Main FastAPI application (300+ lines)
├── 📄 config.py                    # Configuration settings
├── 📄 database.py                  # Database connection utilities
├── 📄 requirements.txt             # Full Python dependencies
├── 📄 requirements-minimal.txt     # Minimal dependencies (Production)
├── 📄 .env                         # Environment variables (Not in Git)
├── 📄 .env.example                 # Environment template
├── 📄 README.md                    # Backend documentation
│
└── 📁 routes/                      # API Route Modules (8 files, ~40 endpoints)
    ├── 📄 farms.py                 # Farm management (6 endpoints, 200+ lines)
    ├── 📄 charts.py                # Statistics & charts (8 endpoints, 250+ lines)
    ├── 📄 diary.py                 # Activity logs (5 endpoints, 180+ lines)
    ├── 📄 qr.py                    # QR code & traceability (3 endpoints, 150+ lines)
    ├── 📄 geojson.py               # GeoJSON map data (6 endpoints, 580+ lines) ⭐ NEW
    ├── 📄 enhanced.py              # Enhanced queries (6 endpoints, 200+ lines)
    ├── 📄 fertilizers.py           # Fertilizer catalog (3 endpoints, 120+ lines)
    └── 📄 pesticides.py            # Pesticide catalog (3 endpoints, 120+ lines)
```

### 📄 Backend Key Files

#### `app.py`

-    **Purpose:** FastAPI application entry point
-    **Responsibilities:**
     -    Initialize FastAPI app
     -    Configure CORS middleware
     -    Register all route modules
     -    Health check endpoint
-    **Key Code:**

     ```python
     from fastapi import FastAPI
     from fastapi.middleware.cors import CORSMiddleware
     from routes import farms, charts, diary, qr, geojson, enhanced, fertilizers, pesticides

     app = FastAPI(title="Agricultural Management API", version="2.0")

     # CORS configuration
     app.add_middleware(CORSMiddleware, ...)

     # Register routers
     app.include_router(farms.router, prefix="/api", tags=["Farms"])
     app.include_router(geojson.router, prefix="/api/geojson", tags=["GeoJSON"])
     # ... more routers
     ```

-    **Lines:** 300+

#### `routes/farms.py`

-    **Purpose:** Farm CRUD operations
-    **Endpoints:**
     ```python
     GET    /api/farms/              # List all farms
     POST   /api/farms/              # Create farm
     GET    /api/farms/{id}          # Get farm by ID
     PUT    /api/farms/{id}          # Update farm
     DELETE /api/farms/{id}          # Delete farm
     GET    /api/farms/code/{code}   # Get farm by code
     ```
-    **Database Tables:**
     -    `nongsan.vung_trong` (main)
     -    `nongsan.tinh`, `nongsan.huyen`, `nongsan.xa` (location)
     -    `nongsan.to_chuc_ca_nhan` (owner)
-    **Lines:** 200+

#### `routes/geojson.py` ⭐ NEW

-    **Purpose:** GeoJSON map data for Leaflet.js
-    **Endpoints:**
     ```python
     GET /api/geojson/provinces          # Province polygons
     GET /api/geojson/districts          # District polygons
     GET /api/geojson/communes           # Commune polygons
     GET /api/geojson/farms/boundaries   # Farm boundaries
     GET /api/geojson/routes/lines       # Province connections
     GET /api/geojson/info/{layer}/{id}  # Click info popup
     ```
-    **Database Queries:**
     -    Uses PostGIS functions (if available)
     -    Falls back to coordinate parsing
     -    Generates GeoJSON FeatureCollection
-    **Response Format:**
     ```json
     {
       "type": "FeatureCollection",
       "features": [
         {
           "type": "Feature",
           "geometry": {
             "type": "Polygon",
             "coordinates": [[[lon, lat], ...]]
           },
           "properties": {
             "id": 1,
             "name": "Lâm Đồng",
             "area": 9800,
             "population": 1200000
           }
         }
       ]
     }
     ```
-    **Lines:** 580+

#### `routes/diary.py`

-    **Purpose:** Activity log management
-    **Endpoints:**
     ```python
     GET    /api/diary/                  # List activities
     POST   /api/diary/                  # Create activity
     GET    /api/diary/{id}              # Get activity
     PUT    /api/diary/{id}              # Update activity
     DELETE /api/diary/{id}              # Delete activity
     GET    /api/diary/farm/{farm_id}    # Get by farm
     ```
-    **Database Tables:**
     -    `nongsan.lich_su_canh_tac` (main)
     -    `nongsan.loai_hoat_dong` (activity types)
     -    `nongsan.phan_bon`, `nongsan.thuoc_bvtv`, `nongsan.giong_cay` (products)
-    **Lines:** 180+

#### `routes/qr.py`

-    **Purpose:** QR code generation and traceability
-    **Endpoints:**
     ```python
     GET /api/qr/generate/{ma_vung}  # Generate QR code image
     GET /api/qr/trace/{ma_vung}     # Trace product (Public API)
     ```
-    **Key Functions:**
     -    Generate QR code PNG image
     -    Return farm info + activity timeline
     -    Public endpoint (no auth required)
-    **Dependencies:** `qrcode`, `PIL`
-    **Lines:** 150+

#### `routes/charts.py`

-    **Purpose:** Dashboard statistics and chart data
-    **Endpoints:**
     ```python
     GET /api/dashboard/stats            # KPI cards
     GET /api/charts/export-markets      # Export market chart
     GET /api/charts/crop-production     # Crop production
     GET /api/charts/facilities-by-type  # Facilities chart
     GET /api/charts/farm-status         # Farm status pie
     GET /api/charts/monthly-activities  # Activity trends
     GET /api/charts/productivity-trend  # Productivity line
     GET /api/charts/pesticide-usage     # Pesticide usage
     ```
-    **Response Format:** Chart.js compatible
-    **Lines:** 250+

### 📦 Dependencies

#### `requirements.txt`

Full dependencies for development:

```txt
fastapi==0.128.0
uvicorn==0.34.0
sqlalchemy==2.0.39
psycopg2-binary==2.9.10
pydantic==2.10.6
pandas==2.3.2
qrcode==8.0
pillow==11.1.0
python-multipart==0.0.20
```

#### `requirements-minimal.txt`

Production minimal dependencies:

```txt
fastapi==0.128.0
uvicorn[standard]==0.34.0
psycopg2-binary==2.9.10
sqlalchemy==2.0.39
pydantic==2.10.6
qrcode==8.0
pillow==11.1.0
```

---

## 🎨 Frontend Structure

```
Frontend/
├── 📄 index.html                   # HTML template (entry point)
├── 📄 package.json                 # npm dependencies & scripts
├── 📄 vite.config.js               # Vite build configuration
├── 📄 tailwind.config.js           # Tailwind CSS configuration
├── 📄 postcss.config.js            # PostCSS configuration
├── 📄 jsconfig.json                # JavaScript IDE configuration
├── 📄 README.md                    # Frontend documentation
├── 📄 check_unused.sh              # Script to check unused components
│
├── 📁 public/                      # Static assets (served as-is)
│   └── favicon.ico
│
└── 📁 src/                         # Source code
    ├── 📄 App.vue                  # Root component (200+ lines)
    ├── 📄 main.js                  # Application entry point
    ├── 📄 STYLING_GUIDE.md         # CSS styling guide
    │
    ├── 📁 assets/                  # CSS & static assets
    │   ├── 📄 main.css             # Main CSS (imports all styles)
    │   └── 📁 styles/
    │       ├── 📄 scrollbar.css    # Custom scrollbar styles
    │       └── 📄 tailwind.css     # Tailwind directives
    │
    ├── 📁 components/              # 🧩 Reusable Components (26 files)
    │   ├── 📄 BarChartComponent.vue           # Bar chart (Chart.js)
    │   ├── 📄 CropDetailsComponent.vue        # Crop details display
    │   ├── 📄 DataTableComponent.vue          # Data table with pagination
    │   ├── 📄 DiaryActivityForm.vue           # Activity form (400+ lines)
    │   ├── 📄 DiaryActivityHistory.vue        # Timeline display
    │   ├── 📄 DiaryActivitySelector.vue       # Activity type selector
    │   ├── 📄 FilterTabs.vue                  # Status filter tabs
    │   ├── 📄 HomeDetailView.vue              # Farm detail view
    │   ├── 📄 HomeListItem.vue                # Farm list item
    │   ├── 📄 LineChartComponent.vue          # Line chart
    │   ├── 📄 MapComponent.vue                # Leaflet map (600+ lines)
    │   ├── 📄 MapLayerControl.vue             # Layer control panel ⭐ NEW
    │   ├── 📄 MapLayerSelector.vue            # Layer selector buttons ⭐ NEW
    │   ├── 📄 PieChartComponent.vue           # Pie chart
    │   ├── 📄 ProductivityLineChart.vue       # Productivity trend chart
    │   ├── 📄 ProductList.vue                 # Product catalog list
    │   ├── 📄 QRModal.vue                     # QR code modal
    │   ├── 📄 QRScanner.vue                   # QR scanner (camera)
    │   ├── 📄 SidebarHeader.vue               # Sidebar header
    │   ├── 📄 StatsBarComponent.vue           # KPI stats bar
    │   └── 📁 icons/                          # Icon components (5 files)
    │       ├── IconCommunity.vue
    │       ├── IconDocumentation.vue
    │       ├── IconEcosystem.vue
    │       ├── IconSupport.vue
    │       └── IconTooling.vue
    │
    ├── 📁 composables/             # 🪝 Business Logic Hooks (6 files)
    │   ├── 📄 statusHelpers.js     # Status utilities (colors, labels)
    │   ├── 📄 useCharts.js         # Chart data fetching logic
    │   ├── 📄 useCropData.js       # Crop data management
    │   ├── 📄 useDiary.js          # Diary CRUD operations (300+ lines)
    │   ├── 📄 useHome.js           # Home page logic
    │   ├── 📄 useLineChartData.js  # Line chart data
    │   └── 📄 useMapLogic.js       # Map logic & GeoJSON (400+ lines)
    │
    ├── 📁 router/                  # Vue Router configuration
    │   └── 📄 index.js             # Route definitions (4 routes)
    │
    └── 📁 views/                   # 📄 Page Components (5 files)
        ├── 📄 AboutView.vue        # About page
        ├── 📄 DiaryPage.vue        # Activity log page (400+ lines)
        ├── 📄 HomeView.vue         # Map view (500+ lines)
        ├── 📄 QuanLyView.vue       # Management dashboard (600+ lines)
        ├── 📄 TraceabilityPage.vue # QR traceability (public, 350+ lines)
        └── 📄 ARCHITECTURE.md      # Views architecture doc
```

### 📄 Frontend Key Files

#### `App.vue`

-    **Purpose:** Root application component
-    **Responsibilities:**
     -    Global layout structure
     -    RouterView for page navigation
     -    Global CSS imports
-    **Lines:** 200+

#### `main.js`

-    **Purpose:** Application entry point
-    **Responsibilities:**
     -    Create Vue app instance
     -    Register router
     -    Mount app to DOM
-    **Key Code:**

     ```javascript
     import { createApp } from "vue";
     import App from "./App.vue";
     import router from "./router";
     import "./assets/main.css";

     createApp(App).use(router).mount("#app");
     ```

-    **Lines:** ~30

#### `router/index.js`

-    **Purpose:** Vue Router configuration
-    **Routes:**
     ```javascript
     [
          { path: "/", name: "home", component: HomeView },
          { path: "/quan-ly", name: "quan-ly", component: QuanLyView },
          { path: "/nhat-ky-canh-tac", name: "diary", component: DiaryPage },
          {
               path: "/truy-xuat/:id",
               name: "traceability",
               component: TraceabilityPage,
          },
     ];
     ```
-    **Lines:** ~60

### 🧩 Component Details

#### `components/MapComponent.vue`

-    **Purpose:** Interactive Leaflet map
-    **Features:**
     -    Leaflet.js integration
     -    GeoJSON layer rendering (Provinces, Districts, Communes, Farms)
     -    Layer control
     -    Popup info on click
     -    Filter by location
-    **Dependencies:**
     -    `leaflet` (npm package)
     -    `useMapLogic` composable
     -    MapLayerControl, MapLayerSelector components
-    **Props:**
     ```javascript
     props: {
       farms: Array,            // Farm markers
       selectedFarm: Object,    // Currently selected farm
       showLayers: Boolean      // Show/hide layer control
     }
     ```
-    **Emits:**
     ```javascript
     emits: ["select-farm", "layer-changed"];
     ```
-    **Lines:** 600+

#### `components/DiaryActivityForm.vue`

-    **Purpose:** Form for creating/editing activity logs
-    **Features:**
     -    Activity type selection
     -    Date picker
     -    Conditional fields (fertilizer, pesticide, seed inputs)
     -    Dosage input with unit
     -    Validation
-    **Dependencies:**
     -    `useDiary` composable
     -    Axios for API calls
-    **Props:**
     ```javascript
     props: {
       vungId: Number,              // Farm ID
       existingActivity: Object,    // For editing
       mode: String                 // 'create' | 'edit'
     }
     ```
-    **Emits:**
     ```javascript
     emits: ["save", "cancel"];
     ```
-    **Lines:** 400+

#### `components/MapLayerControl.vue` ⭐ NEW

-    **Purpose:** Layer control panel for map
-    **Features:**
     -    Toggle layers (Provinces, Districts, Communes, Farms)
     -    Opacity sliders
     -    Layer visibility
     -    Color coding
-    **Props:**
     ```javascript
     props: {
       layers: Object,  // { provinces: true, districts: false, ... }
     }
     ```
-    **Emits:**
     ```javascript
     emits: ["toggle-layer", "change-opacity"];
     ```
-    **Lines:** 200+

#### `components/MapLayerSelector.vue` ⭐ NEW

-    **Purpose:** Quick layer selector buttons
-    **Features:**
     -    Radio buttons for layer selection
     -    Single-select mode
     -    Icons for each layer
-    **Lines:** 150+

### 🪝 Composables Details

#### `composables/useMapLogic.js`

-    **Purpose:** Map logic and GeoJSON data fetching
-    **Functions:**
     ```javascript
     export function useMapLogic() {
       const loadGeoJSON = async (layer) => { ... }
       const fetchProvinces = async () => { ... }
       const fetchDistricts = async () => { ... }
       const fetchCommunes = async () => { ... }
       const fetchFarmBoundaries = async () => { ... }
       const addGeoJSONLayer = (map, geojson, style) => { ... }
       const handleLayerClick = (feature, layer) => { ... }

       return {
         loadGeoJSON,
         fetchProvinces,
         fetchDistricts,
         fetchCommunes,
         fetchFarmBoundaries,
         addGeoJSONLayer,
         handleLayerClick
       }
     }
     ```
-    **API Calls:**
     -    `GET /api/geojson/provinces`
     -    `GET /api/geojson/districts`
     -    `GET /api/geojson/communes`
     -    `GET /api/geojson/farms/boundaries`
-    **Lines:** 400+

#### `composables/useDiary.js`

-    **Purpose:** Activity log CRUD operations
-    **Functions:**
     ```javascript
     export function useDiary() {
       const activities = ref([])
       const loading = ref(false)
       const error = ref(null)

       const fetchActivities = async (farmId) => { ... }
       const createActivity = async (data) => { ... }
       const updateActivity = async (id, data) => { ... }
       const deleteActivity = async (id) => { ... }

       return {
         activities,
         loading,
         error,
         fetchActivities,
         createActivity,
         updateActivity,
         deleteActivity
       }
     }
     ```
-    **API Calls:**
     -    `GET /api/diary/farm/{id}`
     -    `POST /api/diary/`
     -    `PUT /api/diary/{id}`
     -    `DELETE /api/diary/{id}`
-    **Lines:** 300+

#### `composables/useCharts.js`

-    **Purpose:** Chart data fetching for dashboard
-    **Functions:**
     ```javascript
     export function useCharts() {
       const fetchDashboardStats = async () => { ... }
       const fetchFacilitiesByType = async () => { ... }
       const fetchFarmStatus = async () => { ... }
       const fetchMonthlyActivities = async () => { ... }
       const fetchProductivityTrend = async () => { ... }

       return {
         fetchDashboardStats,
         fetchFacilitiesByType,
         fetchFarmStatus,
         fetchMonthlyActivities,
         fetchProductivityTrend
       }
     }
     ```
-    **API Calls:**
     -    `GET /api/dashboard/stats`
     -    `GET /api/charts/facilities-by-type`
     -    `GET /api/charts/farm-status`
     -    `GET /api/charts/monthly-activities`
     -    `GET /api/charts/productivity-trend`
-    **Lines:** 250+

### 📦 Frontend Dependencies

#### `package.json`

```json
{
     "dependencies": {
          "vue": "3.5.13",
          "vue-router": "4.5.0",
          "axios": "1.7.9",
          "chart.js": "4.4.7",
          "leaflet": "1.9.4",
          "qrcode.vue": "3.5.0"
     },
     "devDependencies": {
          "vite": "6.0.5",
          "tailwindcss": "3.4.17",
          "@vitejs/plugin-vue": "5.2.1"
     }
}
```

---

## 🗄️ Database Files

```
Database/
├── 📄 backup_database.sh           # Backup/restore script (150 lines)
├── 📄 cleanup_database.py          # Cleanup script (Jan 10, 2026)
├── 📄 nongsan_schema.sql           # Database schema (if exported)
│
└── 📁 backups/                     # Database backups
    ├── nongsan_db_20260110_143000.sql.gz
    ├── nongsan_db_20260110_150000.sql.gz
    └── ...
```

### 📄 Database Key Files

#### `backup_database.sh`

-    **Purpose:** Database backup and restore utility
-    **Commands:**
     ```bash
     ./backup_database.sh backup          # Create backup
     ./backup_database.sh restore <file>  # Restore from backup
     ./backup_database.sh list            # List all backups
     ```
-    **Features:**
     -    pg_dump with gzip compression
     -    Backup statistics (size, table count)
     -    Color-coded output
     -    Error handling
-    **Configuration:**
     ```bash
     DB_NAME="nongsan_db"
     DB_USER="postgres"
     DB_HOST="localhost"
     DB_PORT="5432"
     BACKUP_DIR="backups/"
     ```
-    **Backup Naming:** `nongsan_db_YYYYMMDD_HHMMSS.sql.gz`
-    **Lines:** 150
-    **Executable:** ✅ `chmod +x backup_database.sh`

#### `cleanup_database.py`

-    **Purpose:** Database cleanup script (executed Jan 10, 2026)
-    **Actions Performed:**
     -    Dropped 10 unused tables
     -    Removed 254 invalid records
     -    Removed 3 duplicates
     -    Migrated ten_hoat_chat → ghi_chu (4,922 records)
     -    Added location FKs
     -    Added coordinate columns (x, y)
-    **Result:** Database optimized from 41 → 31 tables (-24.4%)
-    **Lines:** 500+

---

## 📚 Documentation

```
docs/
├── 📄 DATABASE_DESIGN.md           # Database documentation (1000+ lines)
├── 📄 SYSTEM_ARCHITECTURE.md       # System architecture (800+ lines)
├── 📄 USE_CASES.md                 # Use cases & scenarios (700+ lines)
├── 📄 PROJECT_STRUCTURE.md         # This file
└── 📄 API_DOCUMENTATION.md         # API reference (planned)
```

### 📄 Documentation Files

#### `DATABASE_DESIGN.md`

-    **Purpose:** Complete database documentation for thesis
-    **Sections:**
     1.   Overview
     2.   Entity Relationship Diagram (ERD)
     3.   Table Specifications (All 31 tables)
     4.   Relationships & Foreign Keys
     5.   Views (5 views)
     6.   Data Dictionary
     7.   Indexes & Performance
     8.   Data Integrity
     9.   Change Log
-    **Lines:** 1000+
-    **Audience:** Database administrators, thesis reviewers

#### `SYSTEM_ARCHITECTURE.md`

-    **Purpose:** System architecture documentation
-    **Sections:**
     1.   System Overview
     2.   Architecture Diagrams
     3.   Technology Stack
     4.   Component Details (Frontend + Backend)
     5.   Data Flow
     6.   Security
     7.   Deployment
     8.   Scalability
-    **Lines:** 800+
-    **Audience:** Developers, system architects, thesis reviewers

#### `USE_CASES.md`

-    **Purpose:** Use case documentation
-    **Sections:**
     1.   Actors (4 types)
     2.   Use Case Diagram
     3.   Use Case Specifications (17 use cases)
     4.   Scenarios (3 complete scenarios)
     5.   Use Case Relationships
     6.   Priority Matrix
-    **Lines:** 700+
-    **Audience:** Business analysts, thesis reviewers

---

## 📝 File Naming Conventions

### Backend (Python)

-    **Modules:** `snake_case.py` (e.g., `farms.py`, `geojson.py`)
-    **Classes:** `PascalCase` (e.g., `VungTrong`, `LichSuCanhTac`)
-    **Functions:** `snake_case` (e.g., `get_farms`, `create_activity`)
-    **Constants:** `UPPER_SNAKE_CASE` (e.g., `DATABASE_URL`, `API_VERSION`)
-    **Private:** `_leading_underscore` (e.g., `_internal_helper`)

### Frontend (Vue.js)

-    **Components:** `PascalCase.vue` (e.g., `MapComponent.vue`, `DiaryActivityForm.vue`)
-    **Views:** `PascalCase.vue` (e.g., `HomeView.vue`, `QuanLyView.vue`)
-    **Composables:** `camelCase.js` with `use` prefix (e.g., `useDiary.js`, `useMapLogic.js`)
-    **Utilities:** `camelCase.js` (e.g., `statusHelpers.js`)
-    **Variables:** `camelCase` (e.g., `activities`, `selectedFarm`)
-    **Constants:** `UPPER_SNAKE_CASE` (e.g., `API_BASE_URL`)

### Database

-    **Tables:** `snake_case` (e.g., `vung_trong`, `lich_su_canh_tac`)
-    **Views:** `v_` prefix (e.g., `v_vung_trong_full`, `v_co_so_full`)
-    **Columns:** `snake_case` (e.g., `ma_vung`, `ngay_thuc_hien`)
-    **Constraints:** `{table}_{column}_fk` (e.g., `vung_trong_tinh_id_fk`)
-    **Indexes:** `{table}_{column}_idx` (e.g., `vung_trong_ma_vung_idx`)

### Documentation

-    **Markdown:** `UPPER_SNAKE_CASE.md` (e.g., `DATABASE_DESIGN.md`, `SYSTEM_ARCHITECTURE.md`)
-    **Sections:** Title Case with emoji (e.g., `## 🎯 Overview`)

---

## 🔗 Import/Export Relationships

### Backend Dependencies

```
app.py
 ├── imports → routes/farms.py
 ├── imports → routes/charts.py
 ├── imports → routes/diary.py
 ├── imports → routes/qr.py
 ├── imports → routes/geojson.py
 ├── imports → routes/enhanced.py
 ├── imports → routes/fertilizers.py
 └── imports → routes/pesticides.py

routes/farms.py
 ├── imports → database.py (get_db)
 └── queries → nongsan.vung_trong

routes/geojson.py
 ├── imports → database.py
 └── queries → nongsan.tinh, nongsan.huyen, nongsan.xa, nongsan.vung_trong

routes/diary.py
 ├── imports → database.py
 └── queries → nongsan.lich_su_canh_tac, nongsan.loai_hoat_dong

routes/qr.py
 ├── imports → database.py
 ├── imports → qrcode (library)
 └── queries → nongsan.vung_trong, nongsan.lich_su_canh_tac
```

### Frontend Dependencies

```
main.js
 ├── imports → App.vue
 ├── imports → router/index.js
 └── imports → assets/main.css

App.vue
 └── uses → <RouterView />

router/index.js
 ├── imports → views/HomeView.vue
 ├── imports → views/QuanLyView.vue
 ├── imports → views/DiaryPage.vue
 └── imports → views/TraceabilityPage.vue

views/HomeView.vue
 ├── imports → components/MapComponent.vue
 ├── imports → components/HomeListItem.vue
 ├── imports → composables/useHome.js
 └── imports → composables/useMapLogic.js

views/QuanLyView.vue
 ├── imports → components/StatsBarComponent.vue
 ├── imports → components/BarChartComponent.vue
 ├── imports → components/PieChartComponent.vue
 ├── imports → components/ProductivityLineChart.vue
 └── imports → composables/useCharts.js

views/DiaryPage.vue
 ├── imports → components/DiaryActivityForm.vue
 ├── imports → components/DiaryActivityHistory.vue
 ├── imports → components/DiaryActivitySelector.vue
 └── imports → composables/useDiary.js

views/TraceabilityPage.vue
 ├── imports → components/QRModal.vue
 ├── imports → axios (API calls)
 └── queries → GET /api/qr/trace/{ma_vung}

components/MapComponent.vue
 ├── imports → leaflet (library)
 ├── imports → components/MapLayerControl.vue
 ├── imports → components/MapLayerSelector.vue
 └── imports → composables/useMapLogic.js

composables/useMapLogic.js
 ├── imports → axios
 └── calls → GET /api/geojson/provinces, districts, communes, farms/boundaries

composables/useDiary.js
 ├── imports → axios
 └── calls → GET /api/diary/farm/{id}, POST /api/diary/, PUT /api/diary/{id}, DELETE /api/diary/{id}

composables/useCharts.js
 ├── imports → axios
 └── calls → GET /api/dashboard/stats, /api/charts/*
```

### Database Relationships

```
tinh (Province)
 └── huyen (District)
      └── xa (Commune)
           └── vung_trong (Farm)
                ├── vung_cay_trong (Crop Areas)
                │   └── loai_cay (Crop Types)
                ├── toa_do_vung (Coordinates)
                ├── lich_su_canh_tac (Activity History)
                │   ├── loai_hoat_dong (Activity Types)
                │   ├── phan_bon (Fertilizers)
                │   ├── thuoc_bvtv (Pesticides)
                │   └── giong_cay (Seeds)
                └── chung_nhan (Certifications)

co_so (Facilities)
 ├── co_so_dong_goi (Packaging)
 ├── co_so_phan_bon (Fertilizer)
 ├── co_so_thuoc_bvtv (Pesticide)
 └── co_so_giong (Seed)

to_chuc_ca_nhan (Organizations/Individuals)
 └── vung_trong.chu_so_huu_id (Farm owners)

thi_truong (Markets)
 └── vung_trong_thi_truong (Farm-Market relations)
```

---

## ⚙️ Configuration Files

### Backend Configuration

#### `.env`

```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/nongsan_db

# API
API_TITLE=Agricultural Management API
API_VERSION=2.0
API_DEBUG=True

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Server
HOST=0.0.0.0
PORT=8000
```

#### `requirements.txt`

-    **Purpose:** Full Python dependencies
-    **Usage:** Development environment
-    **Install:** `pip install -r requirements.txt`

#### `requirements-minimal.txt`

-    **Purpose:** Minimal dependencies for production
-    **Usage:** Production deployment
-    **Install:** `pip install -r requirements-minimal.txt`

### Frontend Configuration

#### `vite.config.js`

```javascript
import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
     plugins: [vue()],
     resolve: {
          alias: {
               "@": fileURLToPath(new URL("./src", import.meta.url)),
          },
     },
     server: {
          port: 5173,
          proxy: {
               "/api": {
                    target: "http://localhost:8000",
                    changeOrigin: true,
               },
          },
     },
});
```

#### `tailwind.config.js`

```javascript
module.exports = {
     content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
     theme: {
          extend: {
               colors: {
                    primary: "#10b981",
                    secondary: "#3b82f6",
                    // ... more custom colors
               },
          },
     },
     plugins: [],
};
```

#### `package.json`

```json
{
     "name": "frontend",
     "version": "2.0.0",
     "scripts": {
          "dev": "vite",
          "build": "vite build",
          "preview": "vite preview"
     },
     "dependencies": {
          "vue": "3.5.13",
          "vue-router": "4.5.0",
          "axios": "1.7.9",
          "chart.js": "4.4.7",
          "leaflet": "1.9.4",
          "qrcode.vue": "3.5.0"
     },
     "devDependencies": {
          "vite": "6.0.5",
          "tailwindcss": "3.4.17",
          "@vitejs/plugin-vue": "5.2.1"
     }
}
```

#### `jsconfig.json`

```json
{
     "compilerOptions": {
          "baseUrl": ".",
          "paths": {
               "@/*": ["./src/*"]
          }
     },
     "exclude": ["node_modules", "dist"]
}
```

### Database Configuration

#### PostgreSQL Connection

```bash
# Connection string format
postgresql://[user]:[password]@[host]:[port]/[database]

# Example
postgresql://postgres:password@localhost:5432/nongsan_db
```

#### Database Settings

```sql
-- Schema
CREATE SCHEMA IF NOT EXISTS nongsan;

-- Set search path
SET search_path TO nongsan, public;

-- Character encoding
SET client_encoding = 'UTF8';
```

---

## 📊 File Size Overview

### Backend

```
app.py                      ~10 KB
routes/farms.py             ~8 KB
routes/geojson.py           ~25 KB (largest route file)
routes/charts.py            ~12 KB
routes/diary.py             ~9 KB
routes/qr.py                ~7 KB
routes/enhanced.py          ~10 KB
routes/fertilizers.py       ~6 KB
routes/pesticides.py        ~6 KB
Total Backend Code:         ~100 KB
```

### Frontend

```
App.vue                     ~10 KB
main.js                     ~1 KB
views/HomeView.vue          ~20 KB
views/QuanLyView.vue        ~25 KB
views/DiaryPage.vue         ~18 KB
views/TraceabilityPage.vue  ~15 KB
components/MapComponent.vue ~30 KB (largest component)
composables/useMapLogic.js  ~18 KB
composables/useDiary.js     ~15 KB
Total Frontend Code:        ~300 KB
```

### Documentation

```
README.md                   ~40 KB
DATABASE_DESIGN.md          ~80 KB
SYSTEM_ARCHITECTURE.md      ~60 KB
USE_CASES.md                ~50 KB
PROJECT_STRUCTURE.md        ~45 KB (this file)
Total Documentation:        ~275 KB
```

---

## 🎯 Quick Reference

### Start System

```bash
./start.sh dev
```

### Backup Database

```bash
./Database/backup_database.sh backup
```

### Install Dependencies

```bash
# Backend
cd Backend
pip install -r requirements-minimal.txt

# Frontend
cd Frontend
npm install
```

### Run Tests

```bash
# Backend
cd Backend
pytest tests/

# Frontend
cd Frontend
npm run test
```

### Build Production

```bash
# Frontend
cd Frontend
npm run build
# Output: dist/
```

---

## 📞 Support

For questions about project structure:

-    See [README.md](../README.md) for overview
-    See [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) for technical details
-    See [DATABASE_DESIGN.md](DATABASE_DESIGN.md) for database info

---

**Document Version:** 2.0  
**Last Updated:** January 10, 2026  
**Maintained by:** Development Team

**Made with ❤️ for Master's Thesis 🎓**
