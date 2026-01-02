# 🔧 Hướng Dẫn Debug & Troubleshooting

## 🐛 Các Lỗi Thường Gặp

### 1. Database Connection Failed

**Triệu chứng:**

```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Nguyên nhân:**

-    PostgreSQL không chạy
-    Sai host/port/password
-    Database chưa tồn tại

**Giải quyết:**

```bash
# 1. Check PostgreSQL có chạy không
brew services list | grep postgresql
# hoặc
pg_isready -h localhost -p 5432

# 2. Restart PostgreSQL
brew services restart postgresql@14

# 3. Test kết nối
psql -h localhost -p 5432 -U postgres -d nongsan_db

# 4. Kiểm tra .env
cat Backend/.env | grep DB_
```

---

### 2. Module Not Found Error

**Triệu chứng:**

```
ModuleNotFoundError: No module named 'fastapi'
```

**Nguyên nhân:**

-    Virtual environment chưa activate
-    Package chưa cài

**Giải quyết:**

```bash
# 1. Activate venv
cd Backend
source .venv/bin/activate

# 2. Kiểm tra Python path
which python  # Phải là .venv/bin/python

# 3. Cài lại packages
pip install -r requirements.txt

# 4. Verify
pip list | grep fastapi
```

---

### 3. CORS Policy Error

**Triệu chứng:**

```
Access to fetch at 'http://localhost:8000/api/farms/' from origin 'http://localhost:5173'
has been blocked by CORS policy
```

**Nguyên nhân:**

-    Backend chưa config CORS
-    Frontend origin không trong whitelist

**Giải quyết:**

```python
# Backend/app.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### 4. 422 Unprocessable Entity

**Triệu chứng:**

```json
{
     "detail": [
          {
               "loc": ["body", "ma_vung"],
               "msg": "field required",
               "type": "value_error.missing"
          }
     ]
}
```

**Nguyên nhân:**

-    Request body thiếu field bắt buộc
-    Sai data type
-    Schema không khớp

**Giải quyết:**

```bash
# 1. Check schema required fields
# Backend/schemas.py

# 2. Check request body
curl -X POST http://localhost:8000/api/farms/ \
  -H "Content-Type: application/json" \
  -d '{
    "ma_vung": "REQUIRED",
    "ten_vung": "REQUIRED",
    "dien_tich": 2.5
  }'

# 3. Check Swagger UI để xem schema
# http://localhost:8000/docs
```

---

### 5. Foreign Key Constraint Violation

**Triệu chứng:**

```
sqlalchemy.exc.IntegrityError: (psycopg2.errors.ForeignKeyViolation)
insert or update on table "vung_trong" violates foreign key constraint
```

**Nguyên nhân:**

-    ID reference không tồn tại
-    VD: chu_so_huu_id=999 nhưng không có to_chuc_ca_nhan.id=999

**Giải quyết:**

```sql
-- 1. Check ID có tồn tại không
SELECT id FROM nongsan.to_chuc_ca_nhan WHERE id = 999;

-- 2. Lấy danh sách ID hợp lệ
SELECT id, ten_to_chuc FROM nongsan.to_chuc_ca_nhan;

-- 3. Sử dụng ID tồn tại
INSERT INTO nongsan.vung_trong (ma_vung, ten_vung, chu_so_huu_id)
VALUES ('MSVT001', 'Test', 1);  -- ID=1 phải tồn tại
```

---

### 6. Port Already in Use

**Triệu chứng:**

```
OSError: [Errno 48] Address already in use
```

**Nguyên nhân:**

-    Backend/Frontend đã chạy trên port đó

**Giải quyết:**

```bash
# 1. Tìm process đang dùng port 8000
lsof -i :8000

# Output:
# COMMAND   PID   USER   FD   TYPE
# python  12345  user   3u  IPv4

# 2. Kill process
kill -9 12345

# 3. Hoặc dùng port khác
uvicorn app:app --port 8001
```

---

### 7. Frontend: Cannot Read Property of Undefined

**Triệu chứng:**

```javascript
TypeError: Cannot read property 'ten_vung' of undefined
```

**Nguyên nhân:**

-    API chưa trả về data
-    Async chưa resolve
-    Data structure khác expected

**Giải quyết:**

```javascript
// Bad
const farms = ref([]);
const farmName = farms.value[0].ten_vung;  // ❌ Error nếu empty

// Good - Optional chaining
const farmName = farms.value?.[0]?.ten_vung ?? 'N/A';

// Good - Check before access
if (farms.value && farms.value.length > 0) {
  const farmName = farms.value[0].ten_vung;
}

// Good - v-if in template
<div v-if="farms.length > 0">
  {{ farms[0].ten_vung }}
</div>
```

---

### 8. Duplicate Key Value Violates Unique Constraint

**Triệu chứng:**

```
sqlalchemy.exc.IntegrityError: duplicate key value violates unique constraint "vung_trong_ma_vung_key"
```

**Nguyên nhân:**

-    Cố tạo record với mã đã tồn tại

**Giải quyết:**

```sql
-- 1. Check mã đã tồn tại
SELECT * FROM nongsan.vung_trong WHERE ma_vung = 'MSVT001';

-- 2. Dùng mã khác hoặc update
UPDATE nongsan.vung_trong SET ten_vung = 'New Name' WHERE ma_vung = 'MSVT001';

-- 3. Hoặc xóa record cũ
DELETE FROM nongsan.vung_trong WHERE ma_vung = 'MSVT001';
```

---

### 9. Circular Import Error

**Triệu chứng:**

```
ImportError: cannot import name 'VungTrong' from partially initialized module 'models'
```

**Nguyên nhân:**

-    Model A import Model B, Model B import Model A

**Giải quyết:**

```python
# models/__init__.py
# Import theo thứ tự dependency
from models.to_chuc_ca_nhan import ToChucCaNhan  # No dependencies
from models.loai_cay import LoaiCay              # No dependencies
from models.trang_thai_vung import TrangThaiVung  # No dependencies
from models.vung_trong import VungTrong          # Depends on above
from models.lich_su import LichSuCanhTac         # Depends on VungTrong

# Hoặc dùng foreign_keys explicit
class LichSuCanhTac(Base):
    vung_trong = relationship("VungTrong",
                              back_populates="lich_su_canh_tac",
                              foreign_keys="[LichSuCanhTac.vung_trong_id]")
```

---

### 10. JSON Serialization Error

**Triệu chứng:**

```
TypeError: Object of type Decimal is not JSON serializable
```

**Nguyên nhân:**

-    SQLAlchemy model có Decimal, Date, DateTime
-    FastAPI cần Pydantic schema

**Giải quyết:**

```python
# schemas.py
from decimal import Decimal
from datetime import date, datetime

class VungTrongResponse(BaseModel):
    dien_tich: Decimal  # ✅ Pydantic xử lý Decimal
    ngay_tao: datetime  # ✅ Pydantic xử lý datetime

    model_config = ConfigDict(from_attributes=True)  # ✅ Quan trọng!
```

---

## 🔍 Debug Tools

### 1. Backend Logging

```python
# app.py
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@router.get("/farms/")
async def get_farms():
    logger.debug("Fetching farms...")
    farms = db.query(VungTrong).all()
    logger.debug(f"Found {len(farms)} farms")
    return farms
```

### 2. SQL Query Logging

```python
# database.py
engine = create_engine(
    DATABASE_URL,
    echo=True  # ✅ Print tất cả SQL queries
)
```

### 3. Check API với curl

```bash
# GET request
curl http://localhost:8000/api/farms/

# POST request
curl -X POST http://localhost:8000/api/farms/ \
  -H "Content-Type: application/json" \
  -d '{"ma_vung":"TEST"}'

# Pretty print JSON
curl http://localhost:8000/api/farms/ | python3 -m json.tool

# Save response
curl http://localhost:8000/api/farms/ > response.json
```

### 4. PostgreSQL Debug

```sql
-- Check connections
SELECT * FROM pg_stat_activity WHERE datname = 'nongsan_db';

-- Check table sizes
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'nongsan'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check indexes
SELECT * FROM pg_indexes WHERE schemaname = 'nongsan';

-- Explain query
EXPLAIN ANALYZE
SELECT * FROM nongsan.vung_trong v
JOIN nongsan.to_chuc_ca_nhan t ON v.chu_so_huu_id = t.id;
```

### 5. Frontend DevTools

```javascript
// Console logging
console.log("API response:", farms.value);
console.table(farms.value); // Nice table format

// Network tab: Check request/response
// Vue DevTools: Check component state
```

---

## 📝 Health Check Checklist

```bash
# 1. PostgreSQL
pg_isready -h localhost -p 5432

# 2. Backend
curl http://localhost:8000/api/health

# 3. Frontend
curl http://localhost:5173 | head -5

# 4. Database tables
psql -U postgres -d nongsan_db -c "\dt nongsan.*"

# 5. Sample data
psql -U postgres -d nongsan_db -c "SELECT COUNT(*) FROM nongsan.vung_trong"
```

---

**Last Updated:** 02/01/2026
