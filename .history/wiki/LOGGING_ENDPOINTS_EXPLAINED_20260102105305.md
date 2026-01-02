# 📚 GIẢI THÍCH KHÁI NIỆM: LOGGING VÀ ENDPOINTS

## 1️⃣ LOGGING LÀ GÌ?

### Định nghĩa
**Logging** (Ghi nhật ký) là quá trình ghi lại các sự kiện, hành động, lỗi xảy ra trong ứng dụng vào file hoặc console.

### Mục đích
- **Debug (Gỡ lỗi)**: Tìm nguyên nhân lỗi khi app chạy
- **Monitoring (Giám sát)**: Theo dõi hoạt động của hệ thống
- **Audit (Kiểm toán)**: Ghi lại ai làm gì, khi nào

### Levels (Cấp độ) của Log
```
DEBUG    → Thông tin chi tiết cho developer (VD: "Đang kết nối database...")
INFO     → Thông tin chung (VD: "Server đã start trên port 8000")
WARNING  → Cảnh báo (VD: "Database query chậm: 2.5s")
ERROR    → Lỗi nghiêm trọng (VD: "Không kết nối được PostgreSQL")
CRITICAL → Lỗi cực kỳ nghiêm trọng (VD: "Database bị crash")
```

### Ví dụ trong Python (Backend)
```python
import logging

# Cấu hình logging
logging.basicConfig(
    level=logging.DEBUG,              # Hiển thị từ DEBUG trở lên
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),   # Ghi vào file app.log
        logging.StreamHandler()           # Hiển thị trên console
    ]
)

logger = logging.getLogger(__name__)

# Sử dụng logging
logger.debug("Bắt đầu xử lý request GET /api/farms/")
logger.info("User ID 123 đã login thành công")
logger.warning("Số lượng kết nối database đã đạt 80%")
logger.error("Không tìm thấy vùng trồng với ma_vung = MSVT999")
logger.critical("Database connection pool đã hết!")
```

### Khi nào dùng Logging?
- **Development (Phát triển)**: Dùng DEBUG level để xem flow của code
- **Production (Thực tế)**: Dùng INFO/WARNING/ERROR để theo dõi hệ thống
- **Debugging bug**: Thêm log ở những điểm nghi ngờ có lỗi

### Ví dụ trong FastAPI
```python
from fastapi import FastAPI
import logging

logger = logging.getLogger(__name__)

@router.get("/farms/{farm_id}")
async def get_farm(farm_id: int, db: Session = Depends(get_db)):
    logger.info(f"Request GET /farms/{farm_id}")  # Log request
    
    farm = db.query(VungTrong).filter(VungTrong.id == farm_id).first()
    
    if not farm:
        logger.warning(f"Farm {farm_id} not found")  # Log warning
        raise HTTPException(status_code=404, detail="Not found")
    
    logger.debug(f"Found farm: {farm.ma_vung}")  # Log chi tiết
    return farm
```

### Xem Log ở đâu?
```bash
# Trong terminal khi chạy server
uvicorn app:app --reload

# Output:
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:54321 - "GET /api/farms/ HTTP/1.1" 200 OK

# Trong file log
tail -f logs/backend.log
```

---

## 2️⃣ ENDPOINTS LÀ GÌ?

### Định nghĩa
**Endpoint** là một URL cụ thể mà Frontend có thể gọi để request dữ liệu hoặc thực hiện hành động.

### Cấu trúc Endpoint
```
http://localhost:8000/api/farms/
 └─────┬──────┘ └─┬─┘ └─┬┘ └──┬─┘
     Domain    Port  API  Resource
                      Prefix
```

### HTTP Methods (Phương thức)
```
GET     → Lấy dữ liệu (Read)
POST    → Tạo mới (Create)
PUT     → Cập nhật toàn bộ (Update)
PATCH   → Cập nhật một phần (Partial Update)
DELETE  → Xóa (Delete)
```

### Ví dụ CRUD Endpoints cho Vùng trồng
```
GET    /api/farms/           → List tất cả vùng trồng
GET    /api/farms/123        → Chi tiết vùng ID = 123
POST   /api/farms/           → Tạo vùng mới
PUT    /api/farms/123        → Update toàn bộ vùng 123
DELETE /api/farms/123        → Xóa vùng 123
```

### Endpoint trong FastAPI
```python
from fastapi import APIRouter

router = APIRouter(prefix="/farms", tags=["Farms"])

# Endpoint 1: List farms
@router.get("/")  # → Tạo endpoint GET /api/farms/
async def get_farms():
    return {"message": "List of farms"}

# Endpoint 2: Chi tiết farm
@router.get("/{farm_id}")  # → GET /api/farms/123
async def get_farm(farm_id: int):
    return {"id": farm_id, "name": "Vùng lúa 1"}

# Endpoint 3: Tạo farm mới
@router.post("/")  # → POST /api/farms/
async def create_farm(farm_data: dict):
    return {"message": "Farm created"}
```

### Query Parameters (Tham số truy vấn)
```
GET /api/farms/?skip=0&limit=10&status=active
                └──────────┬────────────┘
                    Query Parameters
```

```python
@router.get("/")
async def get_farms(
    skip: int = 0,           # ?skip=0
    limit: int = 10,         # &limit=10
    status: str = None       # &status=active
):
    # Xử lý logic với parameters
    pass
```

### Path Parameters (Tham số đường dẫn)
```
GET /api/farms/123/diary/456
           └─┬─┘      └─┬──┘
         farm_id    entry_id
```

```python
@router.get("/{farm_id}/diary/{entry_id}")
async def get_diary_entry(farm_id: int, entry_id: int):
    return {"farm": farm_id, "entry": entry_id}
```

### Request Body (Dữ liệu gửi lên)
```python
from pydantic import BaseModel

class FarmCreate(BaseModel):
    ma_vung: str
    ten_vung: str
    dien_tich: float

@router.post("/")
async def create_farm(farm: FarmCreate):
    # farm.ma_vung, farm.ten_vung, farm.dien_tich
    return {"message": "Created", "data": farm}
```

### Cách Frontend gọi Endpoint
```javascript
// Vue 3 - Fetch API
async function getFarms() {
  const response = await fetch('http://localhost:8000/api/farms/');
  const data = await response.json();
  return data;
}

// Tạo farm mới
async function createFarm(farmData) {
  const response = await fetch('http://localhost:8000/api/farms/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(farmData)
  });
  return await response.json();
}
```

---

## 3️⃣ ENDPOINTS TRONG PROJECT NÀY

### Backend Endpoints (34 endpoints)

#### 🌾 Farms (Vùng trồng) - `/api/farms/`
```
GET    /api/farms/              → List farms with filters
GET    /api/farms/{farm_id}     → Chi tiết farm
POST   /api/farms/              → Tạo farm mới
PUT    /api/farms/{farm_id}     → Update farm
DELETE /api/farms/{farm_id}     → Xóa farm
GET    /api/farms/stats         → Thống kê farms
```

#### 📊 Charts (Biểu đồ) - `/api/charts/`
```
GET    /api/charts/dashboard-stats     → Số liệu tổng quan
GET    /api/charts/export-markets      → Biểu đồ thị trường xuất khẩu
GET    /api/charts/crop-production     → Biểu đồ sản lượng cây trồng
GET    /api/charts/productivity-trend  → xu hướng năng suất
GET    /api/charts/farm-status         → Biểu đồ trạng thái vùng
GET    /api/charts/activity-timeline   → Timeline hoạt động
```

#### 📔 Diary (Nhật ký) - `/api/diary/`
```
GET    /api/diary/                  → List nhật ký
GET    /api/diary/{entry_id}        → Chi tiết nhật ký
POST   /api/diary/                  → Tạo nhật ký mới
PUT    /api/diary/{entry_id}        → Update nhật ký
DELETE /api/diary/{entry_id}        → Xóa nhật ký
GET    /api/diary/activity-types/   → Danh sách loại hoạt động
```

#### 🧪 Fertilizers (Phân bón) - `/api/fertilizers/`
```
GET    /api/fertilizers/categories  → Loại phân bón
POST   /api/fertilizers/categories  → Tạo loại mới
GET    /api/fertilizers/            → List phân bón
GET    /api/fertilizers/{id}        → Chi tiết
POST   /api/fertilizers/            → Tạo mới
PUT    /api/fertilizers/{id}        → Update
DELETE /api/fertilizers/{id}        → Xóa
```

#### 💊 Pesticides (Thuốc BVTV) - `/api/pesticides/`
```
GET    /api/pesticides/groups       → Nhóm thuốc
POST   /api/pesticides/groups       → Tạo nhóm
GET    /api/pesticides/             → List thuốc
GET    /api/pesticides/{id}         → Chi tiết
POST   /api/pesticides/             → Tạo mới
PUT    /api/pesticides/{id}         → Update
DELETE /api/pesticides/{id}         → Xóa
```

#### 📱 QR Code - `/api/qr/`
```
GET    /api/qr/generate/{ma_vung}   → Tạo QR code
GET    /api/qr/trace/{ma_vung}      → Public traceability (không cần auth)
```

### Frontend Ports (Cổng)
```
Port 5173  → Vite Dev Server (Vue frontend)
Port 8000  → FastAPI Backend
Port 5432  → PostgreSQL Database
```

### Cách kiểm tra Endpoints
```bash
# 1. Swagger UI (API Documentation tự động)
http://localhost:8000/docs

# 2. Curl command
curl http://localhost:8000/api/farms/ | python3 -m json.tool

# 3. Browser
http://localhost:8000/api/qr/trace/MSVT001
```

---

## 4️⃣ SO SÁNH LOGGING VS ENDPOINTS

| Khía cạnh | Logging | Endpoints |
|-----------|---------|-----------|
| **Là gì** | Ghi lại sự kiện trong code | URL để gọi API |
| **Mục đích** | Debug, monitoring | Giao tiếp Frontend-Backend |
| **Ai dùng** | Developer, System Admin | Frontend, Mobile App, External API |
| **Format** | Text log messages | JSON data |
| **Ví dụ** | "User 123 logged in" | GET /api/users/123 |

---

## 5️⃣ BEST PRACTICES (Kinh nghiệm hay)

### Logging
```python
# ✅ GOOD: Log có context
logger.info(f"User {user_id} created farm {farm.ma_vung}")

# ❌ BAD: Log không rõ ràng
logger.info("Farm created")

# ✅ GOOD: Log lỗi với exception
try:
    db.commit()
except Exception as e:
    logger.error(f"Failed to save farm: {e}", exc_info=True)

# ❌ BAD: Bỏ qua thông tin lỗi
except Exception as e:
    logger.error("Error")
```

### Endpoints
```python
# ✅ GOOD: RESTful naming
GET    /api/farms/           # Danh từ số nhiều
POST   /api/farms/
GET    /api/farms/123
PUT    /api/farms/123
DELETE /api/farms/123

# ❌ BAD: Động từ trong URL
GET /api/getFarms/
POST /api/createFarm/
GET /api/farm/123  # Số ít

# ✅ GOOD: Hierarchical (Phân cấp)
GET /api/farms/123/diary/  # Nhật ký của farm 123

# ❌ BAD: Flat structure
GET /api/diary/?farm_id=123  # Khó đọc hơn
```

---

## 6️⃣ KẾT LUẬN

✅ **Logging** giúp developer:
- Debug code hiệu quả
- Theo dõi hệ thống production
- Phát hiện lỗi sớm

✅ **Endpoints** giúp:
- Frontend gọi Backend một cách chuẩn
- Tách biệt logic giữa các tầng
- Dễ test và document

🎯 **Project này có**:
- 34 endpoints RESTful
- Logging trong backend.log
- Swagger UI để test endpoints
