# Backend API - Agriculture Management System

## 🚀 Setup & Installation

### 1. Activate Virtual Environment

```bash
cd Backend
source .venv/bin/activate  # macOS/Linux
# hoặc
.venv\Scripts\activate     # Windows
```

### 2. Install Dependencies

**Cài đặt minimal (chỉ cần để chạy API):**

```bash
pip install -r requirements-minimal.txt
```

**Hoặc cài đặt full (tất cả packages từ môi trường cũ):**

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Chỉnh sửa file .env theo môi trường của bạn
```

### 4. Run Server

```bash
# Cách 1: Chạy trực tiếp
python app.py

# Cách 2: Dùng uvicorn command
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Server sẽ chạy tại:

-    **API:** `http://localhost:8000`
-    **Interactive Docs (Swagger):** `http://localhost:8000/docs`
-    **Alternative Docs (ReDoc):** `http://localhost:8000/redoc`

## 📡 API Endpoints

### Health Check

```
GET /api/health
```

### Charts Data

```
GET /api/charts/export-markets
GET /api/charts/crop-production
GET /api/charts/productivity-trend
```

### Farms Management

```
GET /api/farms
```

### Diary Management

```
GET  /api/diary
POST /api/diary
```

8000/api/health

# Get export markets data

curl http://localhost:8000/api/charts/export-markets

# Or open in browser

open http://localhost:8000/docs

````

### Connect Frontend

Trong Frontend, uncomment các API calls trong `src/composables/useCharts.js`:

```javascript
const response = await fetch('http://localhost:8

### Connect Frontend

Trong Frontend, uncomment các API calls trong `src/composables/useCharts.js`:

```javascript
const response = await fetch('http://localhost:5000/api/charts/export-markets');
const data = await response.json();
````

## 📁 Project Structure

```
Backend/
├── .venv/                 # Virtual environment (đã tạo)
├── app.py                 # Main Flask application
├── requirements.txt       # Full dependencies
├── requirements-minimal.txt  # Minimal dependencies
├── .env.example          # Environment template
├── .env                  # Your config (gitignored)
├── .gitignore
└── README.md             # This file
```

## 🗄️ Next Steps

1. **Database Setup:** Tạo models với SQLAlchemy
2. **API Routes:** Mở rộng endpoints trong `app.py`
3. **Authentication:** Thêm JWT authentication
4. **Testing:** Viết unit tests với pytest
5. **Documentation:** Thêm Swagger/OpenAPI docs
   astAPI 0.115\*\* - Modern async web framework

-    **Uvicorn** - ASGI server
-    **Pydantic** - Data validation
-    **SQLAlchemy 2.0** - ORM
-    **Pandas** - Data processing
-    **GeoPandas** - Geospatial data

## ✨ FastAPI Features

-    ⚡ **Fast performance** - Built on Starlette and Pydantic
-    📚 **Auto-generated docs** - Swagger UI and ReDoc
-    🔍 **Type hints** - Full Python type hints support
-    ✅ **Data validation** - Automatic request/response validation
-    🔄 **Async support** - Native async/await support
-    **SQLAlchemy 2.0** - ORM
-    **Pandas** - Data processing
-    **GeoPandas** - Geospatial data
