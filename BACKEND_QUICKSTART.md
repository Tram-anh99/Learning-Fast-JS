# ⚡ Quick Start - Backend API

## 🚀 Khởi Động (3 bước)

```bash
# 1. Vào thư mục Backend
cd Backend

# 2. Setup (lần đầu)
./setup.sh

# 3. Start server
./start.sh
```

**✅ Done!** API chạy tại http://localhost:8000

---

## 📚 Xem API Docs

👉 **http://localhost:8000/docs** (Interactive Swagger UI)

---

## 🔗 Database Info

```
Host: localhost:5433
Database: postgres
Schema: nongsan
User: postgres
Password: 123456
```

---

## 🎯 API Endpoints Chính

```
GET  /api/health              # Health check
GET  /api/farms                # Danh sách vùng trồng
GET  /api/charts/dashboard-stats   # Thống kê tổng quan
GET  /api/diary                # Nhật ký canh tác
```

**Full API docs:** [API_INTEGRATION.md](Backend/API_INTEGRATION.md)

---

## 🎨 Frontend Integration

```javascript
// Gọi API từ Frontend
const API_BASE = "http://localhost:8000/api";

async function getFarms() {
     const response = await fetch(`${API_BASE}/farms`);
     return await response.json();
}
```

---

## 🔧 Troubleshooting

```bash
# Lỗi kết nối DB?
./test_db.sh

# Port 8000 bị chiếm?
lsof -ti :8000 | xargs kill -9

# Cài lại dependencies?
./setup.sh
```

---

**Xem chi tiết:** [BACKEND_INTEGRATION_COMPLETE.md](BACKEND_INTEGRATION_COMPLETE.md)
